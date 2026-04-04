# Task: Create Pytest Plugin

## Goal
Build a pytest plugin that discovers replay bundles and runs their assertions as test cases.

## Context
Replay bundles in `replays/` should be automatically discovered and executed as pytest tests. Each bundle's assertions become individual test validations.

## Steps
1. Create `src/firmware_replay_lab/pytest_plugin.py`.
2. Implement a pytest collector that finds `*.json` bundles in a configurable directory.
3. For each bundle, generate test items from its assertions.
4. Each test item loads the bundle, runs `evaluate_bundle()`, and reports pass/fail per assertion.
5. Register the plugin via `pyproject.toml` entry point: `[project.entry-points."pytest11"]`.
6. Add integration tests that use sample bundles.
7. Document usage: `uv run pytest --replay-dir=replays/`.
8. Run `uv run pytest -q` and confirm everything works.

## Constraints
- The plugin must not import Dash or UI modules.
- Keep bundle loading lazy (only load when the test runs).
- Preserve existing test behavior; the plugin should be additive.
