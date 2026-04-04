---
applyTo: "**/*.py"
---

# Python Code Guidelines

- Target Python 3.10+. Use `from __future__ import annotations` for forward references.
- Use `dataclasses` for data structures. Avoid Pydantic unless explicitly approved.
- Type-hint all public function signatures.
- Keep dependencies minimal; the core package must work with zero third-party imports.
- Use `pathlib.Path` instead of `os.path`.
- Prefer `json` from stdlib for bundle I/O.
- Use `uv run pytest` to execute tests; never rely on a globally installed pytest.
- Follow existing code style in `src/firmware_replay_lab/` for naming and structure.
