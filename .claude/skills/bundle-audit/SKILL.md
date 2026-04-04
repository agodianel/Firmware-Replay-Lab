---
name: bundle-audit
description: "Verify replay bundle completeness and schema validity. Use when: auditing a bundle, validating schema, checking bundle quality, reviewing a replay case."
argument-hint: "[path-to-replay-bundle-or-directory]"
---

You are auditing a replay bundle for completeness and correctness.

## Inputs

- Bundle path or directory: $ARGUMENTS

## Tasks

1. Load the bundle using `ReplayBundle.load_json()`.
2. Check metadata completeness: target, firmware_version, board, commit must all be non-empty.
3. Check serial_log has at least one entry with valid timestamp_ms, direction, message fields.
4. Check assertions exist and each has a valid `kind`.
5. Check notes are present and provide useful human context.
6. Report any missing or suspicious fields.
7. If events or mocked_inputs are empty, note whether they should be populated for this failure type.
8. Suggest concrete improvements.

## Rules

- Do not modify the bundle during audit.
- Report findings as a structured checklist.
- Distinguish between hard requirements (metadata fields) and soft recommendations (notes quality).
- Reference the schema spec in `replay_spec/` when available.
