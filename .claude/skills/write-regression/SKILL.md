---
name: write-regression
description: "Turn a replay bundle into a pytest regression test. Use when: writing a test from a bundle, creating regression coverage, adding a test case from a replay."
argument-hint: "[path-to-replay-bundle]"
---

You are converting a replay bundle into a pytest regression test.

## Inputs

- Bundle path: $ARGUMENTS

## Tasks

1. Load the replay bundle using `ReplayBundle.load_json()`.
2. Read its assertions and understand what each one validates.
3. Generate a pytest test function that:
   - Loads the bundle from a fixture path.
   - Calls `evaluate_bundle()` and checks the result.
   - Has a descriptive name reflecting the failure scenario.
4. Place the test in `tests/` with a name matching the bundle scenario.
5. Run `uv run pytest -q` to verify the test passes.
6. If the test should fail (capturing a known bug), mark it with `@pytest.mark.xfail` and explain why.

## Rules

- Do not modify the replay bundle itself.
- Do not add assertions beyond what the bundle specifies.
- Keep test functions focused and readable.
- Import only from `firmware_replay_lab` public API.
