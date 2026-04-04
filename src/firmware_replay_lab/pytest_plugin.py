"""Pytest plugin — auto-discover and run replay bundle assertions.

Discovers *.json bundles in configured directories and runs their
assertions as individual test items.

Register via pyproject.toml:
    [project.entry-points."pytest11"]
    firmware_replay = "firmware_replay_lab.pytest_plugin"
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from .bundle import ReplayBundle


def pytest_addoption(parser: Any) -> None:
    group = parser.getgroup("firmware_replay", "Firmware Replay Lab")
    group.addoption(
        "--replay-dir",
        action="append",
        default=[],
        help="Directory containing replay bundles (can be repeated)",
    )
    group.addoption(
        "--replay-glob",
        default="*.json",
        help="Glob pattern for bundle files (default: *.json)",
    )


def pytest_collect_file(parent: Any, file_path: Path) -> "ReplayFile | None":
    replay_dirs = parent.config.getoption("replay_dir", [])
    glob_pattern = parent.config.getoption("replay_glob", "*.json")

    # If --replay-dir is set, only collect from those directories
    if replay_dirs:
        for rdir in replay_dirs:
            rdir_path = Path(rdir).resolve()
            if file_path.resolve().is_relative_to(rdir_path):
                if file_path.match(glob_pattern):
                    return ReplayFile.from_parent(parent, path=file_path)
        return None

    # Otherwise look for bundles in replays/ or any replay-bundles/ dir
    parts = file_path.parts
    if any(p in ("replays", "replay-bundles", "sample-bundles") for p in parts):
        if file_path.suffix == ".json":
            return ReplayFile.from_parent(parent, path=file_path)

    return None


class ReplayFile(pytest.File):
    def collect(self) -> Any:
        try:
            bundle = ReplayBundle.load_json(self.path)
        except Exception as exc:
            yield ReplayItem.from_parent(
                self,
                name="load",
                bundle=None,
                load_error=str(exc),
            )
            return

        if not bundle.assertions:
            yield ReplayItem.from_parent(
                self, name="no-assertions", bundle=bundle, load_error=None,
            )
            return

        for idx, assertion in enumerate(bundle.assertions):
            kind = assertion.get("kind", "unknown")
            name = f"{kind}[{idx}]"
            yield ReplayItem.from_parent(
                self, name=name, bundle=bundle, load_error=None, assertion_idx=idx,
            )


class ReplayItem(pytest.Item):
    def __init__(
        self,
        name: str,
        parent: Any,
        bundle: ReplayBundle | None,
        load_error: str | None,
        assertion_idx: int | None = None,
        **kwargs: Any,
    ):
        super().__init__(name, parent, **kwargs)
        self._bundle = bundle
        self._load_error = load_error
        self._assertion_idx = assertion_idx

    def runtest(self) -> None:
        if self._load_error:
            raise BundleLoadError(self._load_error)

        assert self._bundle is not None

        if self._assertion_idx is None:
            # no-assertions item — just pass
            return

        # Check specific assertion
        assertion = self._bundle.assertions[self._assertion_idx]
        from .replay import _ASSERTION_HANDLERS

        kind = assertion.get("kind", "")
        handler = _ASSERTION_HANDLERS.get(kind)
        if handler is None:
            raise AssertionError(f"Unknown assertion kind: {kind!r}")

        failure = handler(self._bundle, assertion)
        if failure:
            raise AssertionError(failure)

    def repr_failure(self, excinfo: Any, **kwargs: Any) -> str:
        if isinstance(excinfo.value, BundleLoadError):
            return f"Bundle load error: {excinfo.value}"
        return f"Replay assertion failed: {excinfo.value}"

    def reportinfo(self) -> tuple[Path, int | None, str]:
        return self.path, None, f"replay:{self.name}"


class BundleLoadError(Exception):
    pass
