# Task: Issue Triage

## Goal
Triage incoming issues and classify them for the development team.

## Process
1. Read the issue title and description.
2. Classify into one of: `bug-replay`, `adapter-request`, `schema-change`, `ui-feature`, `docs`, `ci`, `other`.
3. Check if a related replay bundle exists in `replays/`.
4. If the issue describes a firmware failure, suggest creating a replay bundle using the `capture-bug` workflow.
5. Assign appropriate labels.
6. If the issue is a duplicate, link to the original.

## Labels
- `replay-bundle` — involves bundle creation or modification
- `assertion-engine` — involves replay evaluation logic
- `adapter` — involves platform-specific parsing
- `ui` — involves the Dash interface
- `schema` — involves bundle format changes
- `ci` — involves workflow or automation
