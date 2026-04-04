---
name: adapter-scaffold
description: "Scaffold support for a new board or framework adapter. Use when: adding ESP32 support, adding STM32 support, creating a new platform adapter, integrating a new target."
argument-hint: "[platform-name] (e.g. esp32, stm32, nrf52)"
---

You are scaffolding a new platform adapter for Firmware Replay Lab.

## Inputs

- Platform name: $ARGUMENTS

## Tasks

1. Create `src/firmware_replay_lab/adapters/{platform}.py` with:
   - A log parser function that converts platform-specific serial output into `SerialLine` entries.
   - A metadata extractor that identifies firmware version, target, and board from log headers or build info.
   - An event recognizer for platform-specific structured events (e.g. ESP32 panic handler output, STM32 HardFault dumps).
2. Create `tests/test_adapter_{platform}.py` with:
   - A test using a sample log snippet.
   - A roundtrip test: parse → bundle → evaluate.
3. Add a sample log fixture in `tests/fixtures/{platform}/`.
4. Update the adapter registry if one exists.
5. Run `uv run pytest -q` to verify.

## Rules

- Keep adapters thin: parse and normalize, do not interpret.
- Preserve all original log text; normalization adds structure, it does not discard data.
- Use the generic adapter interface pattern from existing adapters.
- Do not add platform-specific dependencies to the core package.
