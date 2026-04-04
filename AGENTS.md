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
| `replay_spec/` | Bundle and assertion schemas (the contract) |
| `src/firmware_replay_lab/` | Core Python package |
| `src/firmware_replay_lab/adapters/` | Platform adapters (ESP32, STM32, JTAG, SWD) |
| `tests/` | Source of truth for behavior (109 tests) |
| `replays/sample-bundles/` | 5 canonical failure examples |
| `replays/community/` | User-contributed anonymized bundles |
| `ui/` | Local browser-based Dash app |
| `.claude/skills/` | Claude Code skills (6 skills) |
| `.github/instructions/` | Copilot instruction files |
| `prompts/` | Antigravity and maintenance prompts |

## Tooling

- Use `uv` for all Python environment, dependency, and task management.
- Run tests with `uv run pytest`.
- Install the project with `uv sync`.
- Lint with `uv run ruff check src/ tests/`.
- Never use `pip install` or `python -m venv` in contributions.

## CLI reference

| Command | Purpose |
|---------|---------||
| `frl capture` | Create a new replay bundle from logs and metadata |
| `frl pack` | Add assertions, notes, or logs to an existing bundle |
| `frl inspect` | Summarize a bundle for humans and agents |
| `frl test` | Run assertions deterministically |
| `frl export` | Export to markdown or JSON |
| `frl validate` | Check bundle schema compliance |
| `frl diff` | Compare two bundles |
| `frl anonymize` | Strip PII before sharing |
| `frl ui` | Launch Dash browser interface |
