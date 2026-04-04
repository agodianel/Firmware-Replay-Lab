---
name: ui-inspect
description: "Propose new UI views or improve log and timeline analysis panels in the Dash interface. Use when: adding a Dash page, improving the UI, building a visualization, adding a timeline view."
argument-hint: "[view-name-or-description]"
---

You are proposing or implementing a Dash UI view for replay inspection.

## Inputs

- View name or description: $ARGUMENTS

## Tasks

1. Identify which replay data the view needs (serial_log, events, assertions, metadata).
2. Design the Dash layout using `dash.html` and `dash.dcc` components.
3. Implement data transformation functions that convert bundle data into visualization-ready format.
4. Create the page module in `ui/pages/{view_name}.py`.
5. Register the page in `ui/app.py`.
6. Add a brief docstring explaining what the view reveals about replay behavior.

## Rules

- The UI visualizes evidence; it does not define test truth.
- Keep data transformations deterministic and testable.
- Do not import from `ui/` in the core `src/firmware_replay_lab/` package.
- Use Dash, not Streamlit.
- Prefer clear, simple layouts over complex dashboards.
- Each page should focus on one analysis perspective.
