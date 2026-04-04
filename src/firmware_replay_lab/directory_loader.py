"""Bundle directory format loader — load replay bundles from replay.yaml-based directories."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .bundle import ReplayBundle, SerialLine, SessionMetadata
from .timestamps import normalize_timestamps


def _load_yaml_as_dict(path: Path) -> dict[str, Any]:
    """Minimal YAML-subset loader for simple key-value and list structures.

    Handles the subset of YAML used in replay bundles without requiring PyYAML.
    Supports: key: value, key: [list], nested indented keys, and - list items.
    """
    result: dict[str, Any] = {}
    current_key = ""
    current_list: list[Any] | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip())

        if stripped.startswith("- "):
            if current_list is not None:
                current_list.append(stripped[2:].strip().strip('"').strip("'"))
            continue

        if ":" in stripped:
            key, _, val = stripped.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")

            if current_list is not None and indent == 0:
                result[current_key] = current_list
                current_list = None

            if not val:
                current_key = key
                current_list = []
            else:
                if current_list is not None:
                    result[current_key] = current_list
                    current_list = None
                result[key] = val

    if current_list is not None:
        result[current_key] = current_list

    return result


def load_bundle_directory(dirpath: str | Path) -> ReplayBundle:
    """Load a replay bundle from a directory with replay.yaml structure."""
    dirpath = Path(dirpath)

    # Load metadata
    metadata_path = dirpath / "metadata.json"
    if metadata_path.exists():
        meta_dict = json.loads(metadata_path.read_text(encoding="utf-8"))
        metadata = SessionMetadata(**meta_dict)
    else:
        replay_yaml = dirpath / "replay.yaml"
        if replay_yaml.exists():
            meta_dict = _load_yaml_as_dict(replay_yaml)
            metadata = SessionMetadata(
                target=meta_dict.get("target", "unknown"),
                firmware_version=meta_dict.get("firmware_version", "unknown"),
                board=meta_dict.get("board", "unknown"),
                commit=meta_dict.get("commit", "unknown"),
            )
        else:
            raise FileNotFoundError(
                f"Neither metadata.json nor replay.yaml found in {dirpath}"
            )

    # Load serial log
    serial_log: list[SerialLine] = []
    serial_path = dirpath / "serial.log"
    if serial_path.exists():
        raw_lines = serial_path.read_text(encoding="utf-8").splitlines()
        for ts, msg in normalize_timestamps(raw_lines):
            if msg.strip():
                serial_log.append(SerialLine(
                    timestamp_ms=ts, direction="device->host", message=msg
                ))

    # Load events
    events: list[dict[str, Any]] = []
    events_path = dirpath / "events.jsonl"
    if events_path.exists():
        for line in events_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                events.append(json.loads(line))

    # Load mocked inputs
    mocked_inputs: list[dict[str, Any]] = []
    inputs_dir = dirpath / "inputs"
    if inputs_dir.is_dir():
        for input_file in sorted(inputs_dir.glob("*.json")):
            mocked_inputs.append(json.loads(input_file.read_text(encoding="utf-8")))

    # Load assertions
    assertions: list[dict[str, Any]] = []
    assertions_jsonl = dirpath / "assertions.jsonl"
    if not assertions and assertions_jsonl.exists():
        for line in assertions_jsonl.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                assertions.append(json.loads(line))

    # Load notes
    notes: list[str] = []
    notes_path = dirpath / "notes.md"
    if notes_path.exists():
        for line in notes_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                notes.append(stripped.lstrip("- "))

    return ReplayBundle(
        metadata=metadata,
        serial_log=serial_log,
        events=events,
        mocked_inputs=mocked_inputs,
        assertions=assertions,
        notes=notes,
    )
