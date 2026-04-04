# Roadmap

## Phase 1 — Core reproducibility (current)

- [x] Define replay bundle schema (JSON)
- [x] Implement CLI skeleton (init-bundle, add-log, add-assertion, replay)
- [x] Parse logs and metadata
- [x] Create sample bundles
- [ ] Add pytest plugin for automatic bundle discovery
- [ ] Bundle validator CLI command

## Phase 2 — Real usefulness

- [ ] ESP32 example integration with real panic/watchdog logs
- [ ] Assertion engine: regex, timing windows, ordering, numeric thresholds
- [ ] Report export (Markdown, JSON summary)
- [ ] CI workflow for replay regression (scaffold added)
- [ ] Bundle directory format (replay.yaml-based)

## Phase 3 — Visual and AI-native layer

- [x] Ship CLAUDE.md, AGENTS.md, and Copilot instructions
- [x] Add Claude skills
- [x] Add Antigravity task prompts
- [ ] Dash UI shell with overview, logs, and timeline pages
- [ ] Optional AI summarization module behind flags

## Phase 4 — Growth

- [ ] STM32 adapter
- [ ] More replay sources (JTAG, SWD trace)
- [ ] Diff and graph analysis across bundles
- [ ] Community bundle contributions
- [ ] Benchmark dataset of real anonymized firmware failures
