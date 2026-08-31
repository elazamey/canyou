# Changelog

All notable changes to this repository are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Owner-signed project constraints** (`docs/CONSTRAINTS.md`): the P-1 package signed in full (Q-5, 2026-08-31) — nine rules + six constraint areas, with a verbatim decision record; Phase-1 scope formulation (a) reaffirmed (Q-6); P-2 identity statement endorsed as a refinement candidate only.
- **Delegated requirements draft** (`docs/REQUIREMENTS.md`): R-1..R-7 for the thin slice, each sourced to signed material only (PRODUCT/CONSTRAINTS) with acceptance criteria; status DOCUMENTED until the owner signs (Q-4 delegation). New `verify_requirements.sh` enforces requirements provenance (no requirement without a valid source; unsigned proposals cannot source requirements).
- **Signed Product Definition** (`docs/PRODUCT.md`): canyou is an Agent Operating Platform; first execution phase is a thin slice — Tool Registry + Policy Gate + one Connector. Owner-signed 2026-08-31, recorded verbatim with source.
- **Unsigned proposal intake log** (`docs/PROPOSALS.md`): P-1 platform constraints package (9-rule set, six constraint areas, five pillars, Phase-1 expansion nomination) and P-2 strategic positioning package (competitive thesis, non-goals, distributed intelligence, candidate identity statement, v0–v3 roadmap) preserved verbatim, explicitly unsigned — awaiting owner decisions Q-5/Q-6.
- **Record-integrity hardening (2026-08-31):** `AGENTS.md` §4 rule 9 (append-only record editing: insert after, structure check before commit, disclose any loss), `docs/DEVELOPMENT.md` procedure with subsection anchors, `verify_records.sh` (entry ordering/uniqueness, Source/Status presence, exact subsection anchors P-1=5/P-2=7/P-3=5, handoff field completeness), and a `bash -n` syntax gate in `verify.sh` so a broken check can never pass silently.
- **Derivation pipeline + requirement-provenance rules enshrined in the contract** (`AGENTS.md`): Product Definition → Requirements → Architecture → Stack → Tasks → Implementation → Verification → Evidence → Commit → Handoff; no requirement without an owner/source, no implementation without a requirement, no VERIFIED without evidence. Status-board vocabulary extended with first-class `NOT STARTED` / `BLOCKED` (exact-token enforced).
- Agent-ready repository baseline: agent operating contract (`AGENTS.md`), work-state files
  (`tasks/CURRENT.md`, `tasks/BACKLOG.md`), continuation protocol (`docs/HANDOFF.md`),
  governance documentation (`docs/`), and a deterministic verification suite (`scripts/verify/`).
- CI workflow content (staged at `.github/pending/ci.yml`) that runs the verification
  suite and shellcheck on push and pull request — activation pending maintainer action (`T-008`).
- Issue templates and a pull request template that require verification evidence.

## [0.0.1] — 2026-08-31

### Added

- Initial commit: `README.md` stub.
