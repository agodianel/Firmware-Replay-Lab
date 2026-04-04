---
name: capture-bug
description: "Guide creation of a replay bundle from raw serial logs, metadata, and engineer notes. Use when: capturing a firmware bug, creating a replay case, converting raw logs into a bundle."
argument-hint: "[path-to-serial-log] [target] [board]"
---

You are creating a new replay bundle from a firmware failure.

## Inputs

- Serial log file or pasted log text: $ARGUMENTS
- Target platform (e.g. esp32, stm32)
- Board identifier
- Firmware version and commit if known
- Any engineer notes about the failure

## Tasks

1. Read the serial log and identify the failure point.
2. Create a `SessionMetadata` with target, board, firmware version, commit, and timestamp.
3. Parse log lines into `SerialLine` entries with timestamps and direction.
4. Identify candidate assertions (crash strings, missing init messages, timeout patterns).
5. Create the replay bundle JSON using the project API.
6. Save to `replays/` with a descriptive directory name: `{failure-type}-{target}-{date}`.
7. Add notes summarizing what happened and why it matters.

## Rules

- Do not fabricate log lines or metadata not present in the source.
- Prefer `contains_text` assertions for crash/panic signatures.
- Ask the user to confirm assertions before finalizing.
- Use `uv run pytest` to verify the bundle loads correctly after creation.
