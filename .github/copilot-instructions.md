# Firmware Replay Lab - Agent Instructions

## Mission

Turn one hard-to-reproduce firmware failure into a permanent regression test artifact.

## Product Direction

- Preserve real device behavior in a portable replay bundle.
- Keep the tool vendor-neutral for ESP32, STM32, and similar targets.
- Design outputs for both human engineers and coding agents.

## Core Concepts

- Capture once on hardware, replay everywhere after.
- Treat a failure as a durable artifact, not an ephemeral debugging moment.
- Prefer structured data over unbounded plain-text logs.

## Engineering Rules

- Keep bundle format backward-compatible when possible.
- Add tests with every behavior change in replay or assertion logic.
- Favor deterministic host-side replay behavior.
- Add concise docs for every CLI command.

## Bundle Expectations

A valid replay bundle should include:

- metadata: target, firmware version, board, commit, environment
- serial_log: timestamped lines with direction
- events: typed structured events where possible
- assertions: explicit expected outcomes for replay validation
- notes: short context for human and agent readers

## CI Intent

Every bug fixed from hardware should result in:

1. a bundle committed to version control (or retained in artifact storage)
2. a replay assertion representing the expected behavior
3. a passing automated test that exercises the replay path
