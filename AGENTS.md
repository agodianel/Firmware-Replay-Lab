# AGENTS.md

This repository is optimized for AI-assisted development.

## Goals for agents

- Help transform raw debug artifacts into structured replay bundles.
- Help maintain schema quality and adapter correctness.
- Help generate regression coverage from real failures.
- Help improve visual debugging workflows when they expose evidence more clearly.

## Constraints

- Do not invent missing hardware facts.
- Do not silently change replay schema semantics.
- Do not replace deterministic test logic with model output.
- Do not add unnecessary abstractions in early versions.
- Do not let the UI become the source of truth over the replay engine.

## Best tasks for agents

- Parser scaffolding.
- Schema validation.
- Markdown documentation.
- Converting notes into structured replay cases.
- Generating test boilerplate from bundle fixtures.
- Building Dash pages for replay inspection.

## Tasks that require extra caution

- Modifying assertion semantics.
- Changing timestamp normalization rules.
- Altering adapter interfaces.
- Auto-fixing failures without replay evidence.
- Inferring conclusions in the UI that are not supported by replay data.

## Important paths

| Path | Purpose |
|------|---------|
| `replay_spec/` | Bundle and assertion schemas |
| `src/firmware_replay_lab/` | Core Python package |
| `tests/` | Source of truth for behavior |
| `replays/sample-bundles/` | Canonical bundle examples |
| `ui/` | Local browser-based Dash app |

## Tooling

- Use `uv` for all Python environment, dependency, and task management.
- Run tests with `uv run pytest`.
- Install the project with `uv sync`.
- Never use `pip install` or `python -m venv` in contributions.
