# Contributing to Firmware Replay Lab

## Setup

```bash
git clone <repo-url>
cd firmware-replay-lab
uv sync
```

## Development workflow

1. Create a branch for your change.
2. Write or update tests first when possible.
3. Make your change in `src/firmware_replay_lab/`.
4. Run tests: `uv run pytest -q`.
5. Lint: `uv run ruff check src/ tests/`.
6. Open a pull request.

## Adding a replay bundle

If your change fixes a firmware bug captured from hardware:

1. Capture a bundle: `uv run frl capture -o replays/{name}/bundle.json -t {target} -fw {version} -b {board} -c {commit} -l {log-file}`
2. Pack more data: `uv run frl pack --bundle replays/{name}/bundle.json --assertion-text "{expected-text}" --note "description"`
3. Inspect: `uv run frl inspect --bundle replays/{name}/bundle.json`
4. Test: `uv run frl test --bundle replays/{name}/bundle.json`
5. Commit the bundle with your PR.

## Contributing a community bundle

Community bundles help build a shared dataset of real firmware failures. To contribute:

1. Capture the failure as a replay bundle (see above).
2. **Anonymize**: `uv run frl anonymize --bundle bundle.json -o bundle-clean.json`
3. **Validate**: `uv run frl validate --bundle bundle-clean.json`
4. **Test assertions**: `uv run frl test --bundle bundle-clean.json`
5. Review the output and confirm no secrets, proprietary symbols, or internal addresses remain.
6. Open a PR adding the bundle to `replays/community/` or use the **Community Bundle Submission** issue template.

### Anonymization checklist

- [ ] No API keys, tokens, or passwords
- [ ] No internal IP addresses or hostnames
- [ ] No proprietary function or variable names
- [ ] No personal email addresses
- [ ] No absolute file paths from your machine
- [ ] You have permission to share this debug artifact

The `frl anonymize` command automatically redacts common patterns (IPs, MACs, emails, tokens, paths), but always review the output manually.

## Adding a platform adapter

Use the `adapter-scaffold` Claude skill or follow the Antigravity prompt in `prompts/antigravity/`.

## Code standards

- Python 3.10+, type hints on public APIs.
- Use `dataclasses`, not Pydantic.
- Keep dependencies minimal.
- Tests are the source of truth for replay behavior.
- The UI visualizes evidence; it does not define test outcomes.
