# Contributing to Firmware Replay Lab

Thank you for your interest in contributing! Whether you're fixing a bug, adding an adapter, or sharing a real firmware failure as a replay bundle, every contribution helps make embedded debugging more reproducible.

## Setup

```bash
git clone https://github.com/agodianel/Firmware-Replay-Lab.git
cd Firmware-Replay-Lab
uv sync
```

> **Important**: Use `uv` for all dependency and environment management. Do not use `pip install` or `python -m venv`.

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

Each adapter implements three functions:

| Function | Purpose |
|----------|---------|
| `parse_serial_log(lines)` | Parse raw log lines into `SerialLine` entries |
| `extract_events(lines)` | Identify structured events (panics, faults, resets) |
| `extract_metadata_hints(lines)` | Detect target, board, or firmware version from logs |

See `src/firmware_replay_lab/adapters/esp32.py` for a reference implementation, or use the `adapter-scaffold` Claude skill.

### Existing adapters

- **ESP32** — ESP-IDF log format, panic/watchdog/backtrace detection
- **STM32** — HardFault, HAL errors, register dumps, assert failures
- **JTAG** — OpenOCD/GDB session output, breakpoints, memory access
- **SWD** — SWO/ITM trace, DWT counters, J-Link/PyOCD output

## Code standards

- Python 3.10+, type hints on public APIs.
- Use `dataclasses`, not Pydantic.
- Keep dependencies minimal — core package requires zero third-party packages.
- Tests are the source of truth for replay behavior.
- The UI visualizes evidence; it does not define test outcomes.
- Run `uv run ruff check src/ tests/` before submitting.

## Getting help

- Browse the [Wiki](https://github.com/agodianel/Firmware-Replay-Lab/wiki) for detailed guides.
- Check existing [Issues](https://github.com/agodianel/Firmware-Replay-Lab/issues) before opening new ones.
- Use the Community Bundle Submission issue template for sharing replay bundles.
