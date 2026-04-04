# Firmware Replay Lab

Turn one hard-to-reproduce firmware failure into a permanent regression test.

Firmware Replay Lab is an open-source toolkit for embedded developers who keep losing time to bugs that only appear on real hardware, disappear when logging is added, or cannot be reproduced in CI. It records real device sessions, converts them into portable replay bundles, and lets developers re-run those failures locally, in pytest, or inside CI without needing the board every time.

The repository is designed to work as both a normal developer tool and an AI-native workspace. Developers should be able to clone it and use Claude Code, Copilot, Antigravity, or other agent environments with strong built-in guidance, reusable skills, and repo-scoped instructions.

***

## Why this repo should exist

Embedded development still has a painful gap compared with mainstream software tooling:

- Bugs often depend on timing, interrupts, peripheral state, noisy inputs, or exact boot order.
- Teams do not always have hardware available to every contributor or every CI job.
- Serial logs alone are not enough to reconstruct what really happened.
- Many firmware bugs are seen once, patched ad hoc, then reappear months later.
- AI coding tools can help, but they need structure, workflows, and project-specific instructions to be consistently useful.

Firmware Replay Lab solves this by making firmware failures captureable, replayable, testable, and understandable.

***

## Core insight

A firmware failure should become an artifact.

Instead of treating a field bug, flaky serial trace, or one-off hardware issue as a disposable debugging event, the repo turns it into a durable replay bundle containing:

- metadata about target, firmware version, board, commit, environment
- serial logs and timestamps
- structured events
- optional mocked sensor/network inputs
- assertions and expected outcomes
- notes for humans and agents

That replay bundle becomes a portable regression unit.

***

## Big promise

**Capture on hardware once. Replay everywhere after.**

This is the line that makes the project memorable.

***

## Who it is for

- ESP32 developers using ESP-IDF or Arduino-style stacks
- STM32 developers with HAL, LL, CubeIDE, or custom build systems
- IoT teams with unstable hardware access across contributors
- startups that need stronger validation before hardware-in-the-loop is mature
- engineers who want AI coding agents to debug with real project context instead of vague prompts

***

## Main pain points solved

### 1. Non-reproducible firmware bugs
A device fails once in the lab or field, but the conditions are hard to recreate.

### 2. Weak CI for firmware
Most firmware repos do not have a meaningful path from real bug to automated regression coverage.

### 3. Hardware scarcity
Not every contributor, reviewer, or agent session has a board attached.

### 4. Debugging knowledge disappears
Important debugging sessions stay in chat logs, notes, or one engineer’s memory.

### 5. AI tools lack structure
Claude, Copilot, or Antigravity can help much more when the repo exposes workflows, instructions, and agent files directly in version control.

### 6. Raw logs are hard to reason about
Developers waste time scrolling text when patterns, timing problems, and failure relationships would be clearer in visual form.

***

## Product vision

Firmware Replay Lab should feel like a missing layer between:

- firmware runtime logs
- host-side test harnesses
- replayable fixtures
- visual debugging tools
- AI-assisted debugging workflows
- CI regression enforcement

It is not a full emulator.
It is not a vendor-specific IDE.
It is not just a prompt collection.

It is a reproducibility system for firmware teams.

***

## v1 scope

The first version should stay narrow and useful.

### CLI commands

- `frl capture` — capture logs, metadata, and optional event streams from a live run
- `frl pack` — build a replay bundle directory from raw artifacts
- `frl inspect` — summarize a replay bundle for humans and agents
- `frl test` — execute replay bundles through pytest adapters
- `frl export` — convert bundles to markdown summaries, JSON, or CI-friendly reports
- `frl ui` — open the local browser-based visual inspection interface

### Replay bundle format

Each replay bundle should be a folder with a clear open spec:

```text
replays/
  wifi-timeout-esp32-2026-04-01/
    replay.yaml
    metadata.json
    serial.log
    events.jsonl
    inputs/
      sensor_feed.json
      mqtt_messages.json
    assertions.yaml
    notes.md
```

### Python core

- bundle parser
- timestamp normalizer
- event replayer
- pytest plugin
- adapters for host-side test integration
- UI data providers for local visualization

### First platform support

- ESP32 first
- STM32 second
- generic adapter interface from day one

***

## Visual debug interface

Firmware Replay Lab should include a local browser-based debugging interface in addition to the CLI.

The purpose of the UI is to make replay bundles easier to inspect than raw logs alone. The interface should be launched locally from Python and open in the developer's browser.

### Suggested launch patterns

- `frl ui`
- `python -m firmware_replay_lab.ui`
- `python ui/app.py`

### Recommended UI stack

Use Dash, not Streamlit.

Dash is a good fit because it supports Python-defined layouts, local browser-based apps, interactive graphs, structured dashboards, and multi-page navigation. It matches the need for timelines, filtered logs, error graphs, and side-by-side replay comparisons.

Python can also open the UI automatically in the default browser after startup using the standard `webbrowser` module.

### Intended views

- replay overview dashboard
- timestamped log explorer with filters
- event timeline
- assertion failure inspector
- diff view between passing and failing bundles
- state transition graph
- grouped error clusters across replay cases
- optional AI triage panel

### UI design principles

- deterministic replay core, visual shell on top
- local-first workflow
- useful without AI services
- optimized for debug triage and replay understanding
- browser UI complements tests, it does not replace tests
- future-friendly for opening CI artifacts locally

***

## AI-native layer

This is where the repo becomes much more interesting than a normal test utility.

The repository should include first-class support for agent-driven development so contributors can use the same project with Claude Code, GitHub Copilot, Antigravity, or other environments.

### Goals of the AI layer

- make the repo self-explaining for agents
- reduce prompt repetition
- standardize debugging and replay workflows
- let contributors run the same high-quality actions through slash commands or agent files
- make AI a force multiplier, not a source of random changes

### AI integrations to include

#### Claude Code support
Use project skills in `.claude/skills/` and a root `CLAUDE.md` so Claude can understand repo architecture, replay bundle rules, coding standards, the visual UI layer, and the expected debugging workflow.

Recommended skills:

- `/capture-bug` — guide creation of a replay from raw logs and metadata
- `/triage-replay` — inspect a replay bundle and propose likely failure zones
- `/write-regression` — turn a replay bundle into a pytest regression test
- `/adapter-scaffold` — scaffold support for a new board or framework
- `/bundle-audit` — verify replay bundle completeness and schema validity
- `/ui-inspect` — propose new UI views or improve log and timeline analysis panels
- `/field-report` — transform engineer notes into a structured replay case

#### GitHub Copilot support
Use `.github/copilot-instructions.md` for repository-wide guidance and optional path-specific instructions in `.github/instructions/*.instructions.md` so Copilot understands bundle schemas, testing rules, replay adapters, and how visual inspection layers relate to the core engine.

Also include `AGENTS.md` at repo root so agent-oriented tools that read common agent instruction files can operate consistently.

#### Antigravity support
The repo should include ready-to-run markdown task files and issue templates that can be pasted into Antigravity sessions with minimal editing. These files should define exact tasks such as implementing a parser, adding a schema validator, extending the pytest plugin, or building a new Dash page.

#### API model support
Support external model use through adapters and environment-driven configuration, for example:

- Anthropic API
- Claude on Vertex AI
- OpenAI-compatible backends when useful
- local Ollama for lightweight summarization or triage

Important principle: AI should assist analysis and workflow generation, but replay execution and test verdicts must stay deterministic.

***

## Repo structure proposal

```text
firmware-replay-lab/
├── README.md
├── LICENSE
├── ROADMAP.md
├── CONTRIBUTING.md
├── CLAUDE.md
├── AGENTS.md
├── .gitignore
├── .env.example
├── .github/
│   ├── copilot-instructions.md
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug-replay-request.md
│   │   └── adapter-request.md
│   ├── instructions/
│   │   ├── python.instructions.md
│   │   ├── schemas.instructions.md
│   │   ├── tests.instructions.md
│   │   └── ui.instructions.md
│   └── workflows/
│       ├── ci.yml
│       └── replay-regression.yml
├── .claude/
│   └── skills/
│       ├── capture-bug/
│       │   └── SKILL.md
│       ├── triage-replay/
│       │   └── SKILL.md
│       ├── write-regression/
│       │   └── SKILL.md
│       ├── adapter-scaffold/
│       │   └── SKILL.md
│       ├── bundle-audit/
│       │   └── SKILL.md
│       └── ui-inspect/
│           └── SKILL.md
├── prompts/
│   ├── antigravity/
│   │   ├── build-parser.md
│   │   ├── add-schema-validator.md
│   │   ├── create-pytest-plugin.md
│   │   └── build-dash-ui.md
│   └── maintenance/
│       ├── issue-triage.md
│       └── release-checklist.md
├── ui/
│   ├── app.py
│   ├── pages/
│   │   ├── overview.py
│   │   ├── logs.py
│   │   ├── timeline.py
│   │   ├── assertions.py
│   │   ├── diff.py
│   │   └── graphs.py
│   └── assets/
├── replay_spec/
│   ├── bundle-schema.yaml
│   ├── assertions-schema.yaml
│   └── format-examples/
├── src/
│   └── firmware_replay_lab/
│       ├── cli.py
│       ├── bundle.py
│       ├── capture/
│       ├── replay/
│       ├── adapters/
│       ├── ai/
│       ├── ui/
│       └── reports/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── examples/
│   ├── esp32/
│   ├── stm32/
│   └── generic/
└── replays/
    └── sample-bundles/
```

***

## Flagship files to ship early

### `README.md`
Must sell the problem in under one minute.

Sections:
- what problem this solves
- why replay beats one-off debugging
- quick start
- sample replay bundle
- visual debug UI
- AI workflows
- supported platforms
- roadmap

### `CLAUDE.md`
Should define:
- project mission
- coding standards
- replay bundle philosophy
- deterministic testing rules
- UI boundaries and responsibilities
- how to add adapters
- what AI can and cannot decide automatically

### `AGENTS.md`
Should provide agent-neutral guidance for tools that understand shared agent instructions.

### `.github/copilot-instructions.md`
Should explain:
- bundle schemas are source of truth
- prefer deterministic tests over speculative helpers
- never invent firmware behavior not represented in fixtures
- when editing adapters, preserve replay format compatibility
- the UI must visualize evidence, not fabricate conclusions

***

## Example agent files

### Example `CLAUDE.md`

```md
# CLAUDE.md

You are working in Firmware Replay Lab.

## Mission
This repository turns real firmware failures into replayable regression assets.

## Core rules
- Prefer deterministic replay logic over heuristic inference.
- Never modify replay bundle schemas casually.
- Keep adapters thin and explicit.
- Every bug fix should try to add or improve a replay case.
- AI may summarize, scaffold, classify, and propose tests, but final replay verdicts must come from deterministic code.
- The UI must visualize replay evidence clearly and must not redefine test truth.

## Important paths
- `replay_spec/` contains bundle and assertion schemas.
- `src/firmware_replay_lab/adapters/` contains platform integrations.
- `ui/` contains the local browser-based Dash app.
- `replays/sample-bundles/` contains canonical examples.
- `tests/` is the source of truth for behavior.

## Preferred workflow
1. Inspect failing replay bundle.
2. Identify missing parser or adapter logic.
3. Add or update tests first where possible.
4. Implement the narrowest change.
5. Improve UI inspection only when it helps expose replay evidence.
6. Export a human-readable report if behavior changes.
```

### Example `AGENTS.md`

```md
# AGENTS.md

This repository is optimized for AI-assisted development.

## Goals for agents
- help transform raw debug artifacts into structured replay bundles
- help maintain schema quality and adapter correctness
- help generate regression coverage from real failures
- help improve visual debugging workflows when they expose evidence more clearly

## Constraints
- do not invent missing hardware facts
- do not silently change replay schema semantics
- do not replace deterministic test logic with model output
- do not add unnecessary abstractions in early versions
- do not let the UI become the source of truth over the replay engine

## Best tasks for agents
- parser scaffolding
- schema validation
- markdown documentation
- converting notes into structured replay cases
- generating test boilerplate from bundle fixtures
- building Dash pages for replay inspection

## Tasks that require extra caution
- modifying assertion semantics
- changing timestamp normalization rules
- altering adapter interfaces
- auto-fixing failures without replay evidence
- inferring conclusions in the UI that are not supported by replay data
```

### Example Claude skill: `.claude/skills/triage-replay/SKILL.md`

```md
---
name: triage-replay
description: Analyze a firmware replay bundle, identify probable failure zones, and suggest deterministic next debugging steps.
argument-hint: [path-to-replay-bundle]
---

You are triaging a firmware replay bundle.

Inputs:
- bundle path: $ARGUMENTS

Tasks:
1. Inspect `replay.yaml`, `metadata.json`, `assertions.yaml`, logs, and events.
2. Summarize what kind of failure occurred.
3. Identify likely fault domains such as parsing, timing, adapter mismatch, state machine regression, or missing fixture coverage.
4. Recommend deterministic next steps.
5. If appropriate, suggest a pytest regression structure.
6. If visual analysis would help, recommend a new or improved Dash view.

Rules:
- Do not claim certainty without evidence from the bundle.
- Quote exact files and fields when making claims.
- Prefer small, testable remediation steps.
```

### Example Copilot instruction file

```md
# .github/copilot-instructions.md

This repository builds deterministic firmware replay tooling.

When suggesting code:
- prefer explicit parsing and validation
- keep replay schemas backward compatible unless asked otherwise
- add tests for every behavioral change
- avoid hidden magic and heavy frameworks
- treat `replay_spec/` as the contract
- do not fabricate device behavior not present in fixtures or logs
- keep the Dash UI separate from replay verdict logic
- prioritize visualizations that clarify real evidence
```

***

## AI-assisted features inside the product

The repo itself can expose optional AI features without making the core dependent on them.

### Safe AI use cases

- summarize long serial logs into a human-readable incident report
- classify likely failure category from a replay bundle
- generate a first draft regression test from bundle contents
- convert freeform lab notes into structured metadata
- propose missing fields in incomplete bundles
- suggest adapter scaffolds for new platforms
- suggest useful new Dash panels for debugging workflows

### Unsafe AI use cases

- deciding pass/fail of replay execution
- fabricating missing device data
- silently rewriting assertions
- replacing protocol-specific parsing with “best guess” model output
- claiming a visual correlation is a proven root cause without deterministic evidence

This separation is important because trust will define adoption.

***

## Suggested v1 implementation roadmap

### Phase 1 — Core reproducibility
- define replay bundle schema
- implement CLI skeleton
- parse logs and metadata
- create sample bundles
- add pytest plugin basics

### Phase 2 — Real usefulness
- ESP32 example integration
- assertion engine
- report export
- CI workflow for replay regression
- bundle validator

### Phase 3 — Visual and AI-native repo layer
- ship `CLAUDE.md`, `AGENTS.md`, and Copilot instructions
- add Claude skills
- add Antigravity task prompts
- add Dash UI shell with overview, logs, and timeline pages
- add optional AI summarization module behind flags

### Phase 4 — Growth
- STM32 adapter
- more replay sources
- richer diff and graph analysis
- community bundle contributions
- benchmark dataset of real anonymized firmware failures

***

## Why this could get stars

This project has a strong chance to attract attention because it combines five things that usually live separately:

- embedded testing pain
- reproducibility tooling
- CI regression value
- visual debugging
- AI-native developer workflow files

The result is more interesting than a plain embedded utility and more useful than a generic AI prompt repo.

People can adopt only the deterministic replay core.
People can use the local Dash UI for replay inspection.
People can also adopt the AI workflow layer if they use Claude, Copilot, or Antigravity.
That modularity is a strength.

***

## Launch positioning

### One-line pitch
**Capture once on hardware. Replay forever in tests, CI, and visual debugging.**

### Alternative pitches
- Turn flaky firmware failures into portable regression bundles.
- A reproducibility and visual debug layer for embedded teams.
- Replay real device failures without needing the board every time.
- AI-native firmware debugging with deterministic replay at the core.

### Who will share it
- embedded developers on GitHub
- ESP32 and STM32 communities
- firmware engineers frustrated by weak CI
- developers experimenting with Claude Code and Copilot repo instructions

***

## First release checklist

- clear README with one concrete example
- one sample ESP32 replay bundle
- one pytest regression demo
- one screenshot or asciinema of capture → inspect → test
- one working Dash page for local replay inspection
- `CLAUDE.md`, `AGENTS.md`, and Copilot instructions committed from day one
- 3 to 5 Claude skills for common workflows
- issue templates for replay submissions and adapter requests
- roadmap with narrow believable milestones

***

## Non-goals

To keep the project sharp, explicitly avoid these in the beginning:

- full hardware emulation
- vendor lock-in
- giant framework abstractions
- “AI decides everything” workflow
- pretending to support every MCU immediately
- turning the UI into a bloated observability platform too early

***

## Recommended next files to draft

1. `README.md`
2. `CLAUDE.md`
3. `AGENTS.md`
4. `.github/copilot-instructions.md`
5. first 3 skill files in `.claude/skills/`
6. replay bundle schema draft
7. Antigravity implementation prompts
8. Dash UI architecture note

***

## Final principle

This repo should feel serious, practical, and a little ahead of the curve.

Not “AI for firmware” in a vague marketing sense.
Not “yet another test helper.”

It should feel like a real missing tool:
**a deterministic firmware replay system with first-class visual and AI workflows around it.**
