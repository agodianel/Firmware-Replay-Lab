---
name: triage-replay
description: "Analyze a firmware replay bundle, identify probable failure zones, and suggest deterministic next debugging steps. Use when: triaging a replay, diagnosing a failure, inspecting a bundle."
argument-hint: "[path-to-replay-bundle]"
---

You are triaging a firmware replay bundle.

## Inputs

- Bundle path: $ARGUMENTS

## Tasks

1. Inspect bundle metadata, serial log, events, assertions, and notes.
2. Summarize what kind of failure occurred.
3. Identify likely fault domains: parsing, timing, adapter mismatch, state machine regression, or missing fixture coverage.
4. Recommend deterministic next steps.
5. If appropriate, suggest a pytest regression structure.
6. If visual analysis would help, recommend a new or improved Dash view.

## Rules

- Do not claim certainty without evidence from the bundle.
- Quote exact files and fields when making claims.
- Prefer small, testable remediation steps.
- Never fabricate device behavior not present in the log.
