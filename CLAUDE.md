# CLAUDE.md

You are working in Firmware Replay Lab.

## Mission

This repository turns real firmware failures into replayable regression assets.

**Capture once on hardware. Replay everywhere after.**

## Core rules

- Prefer deterministic replay logic over heuristic inference.
- Never modify replay bundle schemas casually.
- Keep adapters thin and explicit.
- Every bug fix should try to add or improve a replay case.
- AI may summarize, scaffold, classify, and propose tests, but final replay verdicts must come from deterministic code.
- The UI must visualize replay evidence clearly and must not redefine test truth.

## Important paths

| Path | Purpose |
|------|---------|
| `replay_spec/` | Bundle and assertion schemas (the contract) |
| `src/firmware_replay_lab/` | Core package: bundle, capture, replay, CLI |
| `src/firmware_replay_lab/adapters/` | Platform adapters (ESP32, STM32, JTAG, SWD) |
| `ui/` | Local browser-based Dash app |
| `replays/sample-bundles/` | 5 canonical failure examples |
| `replays/community/` | User-contributed anonymized bundles |
| `tests/` | Source of truth for behavior (109 tests) |

## Coding standards

- Python 3.10+, type hints on public APIs.
- Use `uv` for all environment and dependency management.
- Keep dependencies minimal; the core must work with zero third-party packages.
- Use `dataclasses` for data structures, not Pydantic (keep lightweight).
- Tests live in `tests/`; run with `uv run pytest`.

## Preferred workflow

1. Inspect failing replay bundle.
2. Identify missing parser or adapter logic.
3. Add or update tests first where possible.
4. Implement the narrowest change.
5. Improve UI inspection only when it helps expose replay evidence.
6. Export a human-readable report if behavior changes.

## What AI should not do

- Decide pass/fail of replay execution.
- Fabricate missing device data.
- Silently rewrite assertions.
- Replace protocol-specific parsing with "best guess" model output.
- Claim a visual correlation is a proven root cause without deterministic evidence.
