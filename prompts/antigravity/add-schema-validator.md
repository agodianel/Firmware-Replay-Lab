# Task: Add Schema Validator

## Goal
Implement a bundle schema validator that checks replay bundles for required fields, correct types, and structural integrity.

## Context
Replay bundles must include metadata (target, firmware_version, board, commit), serial_log entries with timestamp_ms/direction/message, and assertions with a valid `kind`. There is no runtime validation today.

## Steps
1. Create `src/firmware_replay_lab/validator.py`.
2. Implement `validate_bundle(bundle: ReplayBundle) -> list[str]` that returns a list of error messages (empty = valid).
3. Check metadata: all required fields non-empty.
4. Check serial_log: each entry has timestamp_ms >= 0, direction is a known value, message is non-empty.
5. Check assertions: each has a `kind` that is a recognized type.
6. Optionally warn about empty notes or events.
7. Add tests in `tests/test_validator.py`.
8. Wire the validator into the CLI as `firmware-replay validate --bundle path`.
9. Run `uv run pytest -q` and confirm all tests pass.

## Constraints
- Validation must be deterministic, no network calls.
- Return structured error messages, not exceptions.
- Do not modify the bundle during validation.
