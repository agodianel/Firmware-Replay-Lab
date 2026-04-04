---
applyTo: "replay_spec/**,**/*schema*,**/bundle*"
---

# Schema and Bundle Guidelines

- `replay_spec/` is the contract for replay bundle structure.
- Never change schema semantics without updating version fields and migration logic.
- Keep bundle format backward-compatible when possible.
- A valid bundle must include: metadata, serial_log, events, assertions, notes.
- Metadata must contain: target, firmware_version, board, commit.
- Serial log entries must have: timestamp_ms, direction, message.
- Assertions must have a `kind` field; known kinds: `contains_text`, `event_count`.
- Do not add required fields without a schema migration path.
- Test every schema change with a roundtrip (save → load → assert equality).
