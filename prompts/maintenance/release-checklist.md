# Task: Release Checklist

## Goal
Ensure all quality gates are met before tagging a release.

## Checklist
- [ ] All tests pass: `uv run pytest -q`
- [ ] No lint errors: `uv run ruff check src/ tests/`
- [ ] Version bumped in `pyproject.toml`
- [ ] ROADMAP.md updated with completed milestones
- [ ] README.md reflects current CLI commands and features
- [ ] Sample bundles in `replays/sample-bundles/` load and replay correctly
- [ ] CLAUDE.md and AGENTS.md are current
- [ ] Claude skills reference correct paths and APIs
- [ ] CI workflows pass on main branch
- [ ] CONTRIBUTING.md reflects current development workflow
- [ ] Changelog entry written for this version

## Post-release
- [ ] Tag the release: `git tag v{version}`
- [ ] Push tags: `git push --tags`
- [ ] Announce in relevant channels
