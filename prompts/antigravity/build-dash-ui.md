# Task: Build Dash UI Shell

## Goal
Create the initial Dash application with an overview page and log explorer for local replay bundle inspection.

## Context
The UI should be a local browser-based Dash app launched via `frl ui` or `uv run python -m firmware_replay_lab.ui`. It complements the CLI and tests by providing visual analysis of replay bundles.

## Steps
1. Add `dash` to project dependencies.
2. Create `ui/app.py` with a multi-page Dash app shell.
3. Create `ui/pages/overview.py` — dashboard showing bundle metadata, assertion summary, log line count.
4. Create `ui/pages/logs.py` — timestamped log explorer with text filtering.
5. Add auto-browser-open on startup using `webbrowser.open()`.
6. Add a `--bundle` argument for specifying which bundle to inspect.
7. Wire the UI launch into the CLI as the `frl ui` command.
8. Test that the app starts without errors.

## Constraints
- Use Dash, not Streamlit.
- Keep UI code in `ui/`, not in `src/firmware_replay_lab/`.
- The UI reads bundles but never modifies them.
- Each page should be a separate module in `ui/pages/`.
