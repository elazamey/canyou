# Changelog

All notable changes to this repository are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Agent-ready repository baseline: agent operating contract (`AGENTS.md`), work-state files
  (`tasks/CURRENT.md`, `tasks/BACKLOG.md`), continuation protocol (`docs/HANDOFF.md`),
  governance documentation (`docs/`), and a deterministic verification suite (`scripts/verify/`).
- CI workflow content (staged at `.github/pending/ci.yml`) that runs the verification
  suite and shellcheck on push and pull request — activation pending maintainer action (`T-008`).
- Issue templates and a pull request template that require verification evidence.

## [0.0.1] — 2026-08-31

### Added

- Initial commit: `README.md` stub.
