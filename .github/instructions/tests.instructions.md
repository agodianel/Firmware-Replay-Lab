---
applyTo: "tests/**"
---

# Test Guidelines

- Tests are the source of truth for replay behavior.
- Every behavioral change in replay or assertion logic must include a test.
- Use `tmp_path` fixture for file I/O tests; never write to the repo tree.
- Keep test functions focused: one assertion concept per test.
- Name tests descriptively: `test_replay_fails_when_text_missing`.
- Do not mock the replay engine itself; test it end-to-end through `evaluate_bundle`.
- Run tests with `uv run pytest -q`.
- Place test fixtures in `tests/fixtures/` when bundle files are needed.
