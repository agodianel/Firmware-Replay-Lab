---
applyTo: "ui/**"
---

# UI Guidelines

- The UI uses Dash for local browser-based replay inspection.
- The UI visualizes evidence; it does not define test truth.
- Keep UI code separate from replay verdict logic in `src/firmware_replay_lab/`.
- Never import UI modules from the core package.
- Prefer deterministic data transformations over live queries.
- Each Dash page should focus on one view: overview, logs, timeline, assertions, diff, or graphs.
- Launch with `uv run python -m firmware_replay_lab.ui` or `frl ui`.
- Use the `webbrowser` module to auto-open the browser on startup.
