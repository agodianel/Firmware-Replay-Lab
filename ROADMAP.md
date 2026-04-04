# Roadmap

All four initial phases are complete. The project is fully functional for capturing, replaying, and validating firmware failures across ESP32, STM32, JTAG, and SWD targets.

## Phase 1 — Core reproducibility ✅

- [x] Define replay bundle schema (JSON)
- [x] Implement CLI skeleton (capture, pack, inspect, test, export)
- [x] Parse logs and metadata
- [x] Create sample bundles
- [x] Add pytest plugin for automatic bundle discovery
- [x] Bundle validator CLI command (`frl validate`)
- [x] Bundle directory format loader (replay.yaml / metadata.json)

## Phase 2 — Real usefulness ✅

- [x] ESP32 adapter with real panic/watchdog/backtrace parsing
- [x] Assertion engine: regex, timing windows, ordering, numeric thresholds
- [x] Report export (Markdown, JSON summary)
- [x] CI workflow for replay regression
- [x] Bundle directory format (folder-based loading)
- [x] Timestamp normalizer across log formats
- [x] Bundle diff analysis (`frl diff`)

## Phase 3 — Visual and AI-native layer ✅

- [x] Ship CLAUDE.md, AGENTS.md, and Copilot instructions
- [x] Add Claude skills
- [x] Add Antigravity task prompts
- [x] Dash UI shell with overview, logs, timeline, and assertions pages
- [x] `frl ui` command to launch browser-based inspection
- [x] Optional AI summarization module behind flags (OpenAI, Anthropic, Ollama)

## Phase 4 — Growth ✅

- [x] STM32 adapter with HardFault/HAL error parsing
- [x] More replay sources (JTAG, SWD trace adapters)
- [x] Diff and graph analysis across bundles
- [x] Community bundle contributions (issue template, anonymizer, guide)
- [x] Benchmark dataset of real anonymized firmware failures (5 bundles)

---

## What's next

Ideas for future development. Contributions welcome.

- [ ] Multi-bundle timeline overlay in the Dash UI
- [ ] RTOS-aware event parsing (FreeRTOS task states, queue events)
- [ ] Bundle import from Segger SystemView / Percepio Tracealyzer
- [ ] Remote capture agent over SSH or serial-over-network
- [ ] Bundle versioning and migration tooling
- [ ] Flaky failure detection across repeated captures
- [ ] Integration with GitHub Actions for auto-bundle on CI failure
- [ ] Protocol-specific adapters (CAN, I2C, SPI bus analyzers)
