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

1. Create a bundle: `uv run firmware-replay init-bundle --output replays/{name}/bundle.json --target {target} --firmware-version {version} --board {board} --commit {commit}`
2. Add the serial log: `uv run firmware-replay add-log --bundle replays/{name}/bundle.json --log-file {log-file}`
3. Add assertions: `uv run firmware-replay add-assertion --bundle replays/{name}/bundle.json --kind contains_text --text "{expected-text}"`
4. Verify: `uv run firmware-replay replay --bundle replays/{name}/bundle.json`
5. Commit the bundle with your PR.

## Adding a platform adapter

Use the `adapter-scaffold` Claude skill or follow the Antigravity prompt in `prompts/antigravity/`.

## Code standards

- Python 3.10+, type hints on public APIs.
- Use `dataclasses`, not Pydantic.
- Keep dependencies minimal.
- Tests are the source of truth for replay behavior.
- The UI visualizes evidence; it does not define test outcomes.
