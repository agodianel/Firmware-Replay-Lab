# Firmware Replay Lab

Capture firmware failures once on hardware, replay them everywhere.

Firmware Replay Lab turns hard-to-reproduce device failures into portable replay bundles that can run locally and in CI.

## What this baseline includes

- A replay bundle format with metadata, serial logs, events, assertions, and notes
- A Python API for creating, loading, and saving bundles
- A small CLI for initializing bundles, attaching captured logs, adding assertions, and replaying checks
- Unit tests for bundle persistence and replay evaluation

## Install

```bash
uv sync
```

## CLI quickstart

```bash
uv run firmware-replay init-bundle \
  --output bundles/example.json \
  --target esp32 \
  --firmware-version v1.2.3 \
  --board devkitc \
  --commit abc123

uv run firmware-replay add-log \
  --bundle bundles/example.json \
  --log-file logs/serial.txt

uv run firmware-replay add-assertion \
  --bundle bundles/example.json \
  --kind contains_text \
  --text "PANIC"

uv run firmware-replay replay --bundle bundles/example.json
```

## Run tests

```bash
uv run pytest
```

## Bundle schema (JSON)

- `metadata`: target, firmware version, board, commit, capture timestamp, environment
- `serial_log`: timestamped lines from UART or similar channels
- `events`: structured events from host probes or adapters
- `mocked_inputs`: optional mocked sensor/network values
- `assertions`: expected outcomes used during replay
- `notes`: short context for human and agent readers

## AI workflows

This repo includes first-class AI agent support:

- **Claude Code**: skills in `.claude/skills/` and root `CLAUDE.md`
- **GitHub Copilot**: instructions in `.github/copilot-instructions.md` and `.github/instructions/`
- **Antigravity**: task prompts in `prompts/antigravity/`
- **Agent-neutral**: root `AGENTS.md` for any compatible tool

## Supported platforms

- ESP32 (first target)
- STM32 (second target)
- Generic adapter interface from day one
- `notes`: human and agent context
