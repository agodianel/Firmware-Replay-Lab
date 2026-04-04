# Task: Build Replay Bundle Parser

## Goal
Implement or extend the replay bundle parser so it can load bundles from both JSON files and YAML-based replay directories.

## Context
The current parser in `src/firmware_replay_lab/bundle.py` handles JSON bundles. The spec also defines a directory-based format with `replay.yaml`, `metadata.json`, `serial.log`, `events.jsonl`, `assertions.yaml`, and `notes.md`.

## Steps
1. Read the current `ReplayBundle` class in `src/firmware_replay_lab/bundle.py`.
2. Add a `load_directory(path)` class method that reads a replay directory.
3. Parse `replay.yaml` for top-level bundle config.
4. Parse `metadata.json` into `SessionMetadata`.
5. Parse `serial.log` into `SerialLine` entries (one per line, with timestamp extraction).
6. Parse `events.jsonl` into the events list.
7. Parse `assertions.yaml` into the assertions list.
8. Read `notes.md` into the notes list.
9. Add tests in `tests/test_bundle.py` for directory-based loading.
10. Run `uv run pytest -q` and confirm all tests pass.

## Constraints
- Do not break existing JSON bundle loading.
- Use only stdlib modules (json, pathlib); add PyYAML only if it is already a dependency.
- Keep the parser deterministic and explicit.
