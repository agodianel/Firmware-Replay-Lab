# Firmware Replay Lab

<!-- <p align="center">
  <img src="docs/assets/banner.png" alt="Firmware Replay Lab" width="500">
</p> -->

<h3 align="center">🔁 Firmware Replay Lab</h3>

<p align="center">
  <strong>Capture once on hardware. Replay everywhere after.</strong>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="license MIT"></a>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="python 3.10+">
  <img src="https://img.shields.io/badge/CI-passing-brightgreen.svg" alt="CI passing">
  <img src="https://img.shields.io/badge/tests-109%20passed-brightgreen.svg" alt="tests 109 passed">
  <img src="https://img.shields.io/badge/bundles-5%20samples-orange.svg" alt="bundles 5 samples">
  <img src="https://img.shields.io/badge/adapters-ESP32%20%7C%20STM32%20%7C%20JTAG%20%7C%20SWD-blueviolet.svg" alt="adapters">
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> ·
  <a href="#cli-commands">CLI Commands</a> ·
  <a href="#visual-debug-ui">Visual UI</a> ·
  <a href="#ai-workflows">AI Workflows</a> ·
  <a href="#supported-platforms">Platforms</a> ·
  <a href="CONTRIBUTING.md">Contributing</a> ·
  <a href="ROADMAP.md">Roadmap</a>
</p>

---

Firmware Replay Lab turns hard-to-reproduce device failures into portable replay bundles that run locally, in pytest, and in CI — without needing the board every time.

## The problem

Embedded bugs depend on timing, interrupts, peripheral state, and exact boot sequences. They appear once in the lab, vanish when logging changes, and reappear months later. Serial logs alone cannot reconstruct what happened. Most firmware repos have no path from a real bug to automated regression coverage.

## Why replay beats one-off debugging

A firmware failure should become an **artifact**, not a disposable debugging moment. Firmware Replay Lab converts a raw capture session into a durable bundle containing metadata, timestamped serial logs, structured events, assertions, and notes. That bundle becomes a portable regression unit you can re-run anywhere.

## Quick start

```bash
uv sync
```

### Capture a failure

```bash
uv run frl capture \
  -o replays/wifi-timeout/bundle.json \
  -t esp32 -fw v2.1.0 -b devkitc -c a1b2c3d \
  -l logs/serial.log
```

### Pack more data into the bundle

```bash
uv run frl pack \
  --bundle replays/wifi-timeout/bundle.json \
  --assertion-text "WiFi connection timeout" \
  --note "AP was powered on late during cold boot"
```

### Inspect the bundle

```bash
uv run frl inspect --bundle replays/wifi-timeout/bundle.json
```

### Run assertions

```bash
uv run frl test --bundle replays/wifi-timeout/bundle.json
```

### Export a report

```bash
uv run frl export --bundle replays/wifi-timeout/bundle.json --format markdown
```

## Sample replay bundle

```json
{
  "metadata": {
    "target": "esp32",
    "firmware_version": "v2.1.0",
    "board": "devkitc-v4",
    "commit": "a1b2c3d",
    "captured_at": "2026-04-01T14:30:00+00:00"
  },
  "serial_log": [
    {"timestamp_ms": 0, "direction": "device->host", "message": "rst:0x1 (POWERON_RESET)"},
    {"timestamp_ms": 5000, "direction": "device->host", "message": "E (5012) wifi: wifi_connect: sta is not started"},
    {"timestamp_ms": 10001, "direction": "device->host", "message": "abort() was called at PC 0x400d1234 on core 0"}
  ],
  "assertions": [
    {"kind": "contains_text", "text": "WiFi connection timeout"},
    {"kind": "event_count", "event_type": "wifi_error", "min_count": 1}
  ],
  "notes": ["ESP32 fails WiFi connect on cold boot when AP is not yet broadcasting."]
}
```

## CLI commands

| Command | Description |
|---------|-------------|
| `frl capture` | Capture logs, metadata, and events into a new replay bundle |
| `frl pack` | Add logs, assertions, or notes to an existing bundle |
| `frl inspect` | Summarize a replay bundle for humans and agents |
| `frl test` | Execute replay bundle assertions as deterministic checks |
| `frl export` | Export bundle to markdown summary or JSON report |
| `frl validate` | Validate a bundle against the schema |
| `frl diff` | Compare two replay bundles side by side |
| `frl anonymize` | Strip sensitive data from a bundle for safe sharing |
| `frl ui` | Open local browser-based visual inspection interface |

## Run tests

```bash
uv run pytest
```

## Visual debug UI

A local browser-based Dash interface for inspecting replay bundles visually — timelines, filtered logs, assertion results, and side-by-side comparisons.

```bash
uv run frl ui
# or with options:
uv run frl ui --bundle-dir replays/sample-bundles --port 8050
```

## Bundle format

Each replay bundle can be a single JSON file or a directory:

```text
replays/wifi-timeout-esp32-2026-04-01/
  replay.yaml
  metadata.json
  serial.log
  events.jsonl
  inputs/
    sensor_feed.json
    mqtt_messages.json
  assertions.yaml
  notes.md
```

## AI workflows

This repo includes first-class AI agent support:

- **Claude Code**: skills in `.claude/skills/` and root `CLAUDE.md`
- **GitHub Copilot**: instructions in `.github/copilot-instructions.md` and `.github/instructions/`
- **Antigravity**: task prompts in `prompts/antigravity/`
- **Agent-neutral**: root `AGENTS.md` for any compatible tool

## Supported platforms

- **ESP32** — ESP-IDF log parsing, panic/watchdog/backtrace detection
- **STM32** — HardFault, HAL error, register dump, assert parsing
- **JTAG** — OpenOCD/GDB debug session logs
- **SWD** — SWO/ITM trace, DWT data, J-Link/PyOCD output
- Generic adapter interface for new platforms

## Roadmap

See [ROADMAP.md](ROADMAP.md) for milestones.

## License

MIT
- `notes`: human and agent context
