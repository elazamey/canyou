# Operations

How this repository is operated and kept trustworthy. Audience: maintainers and agents performing maintenance tasks.

## Continuous Integration

Workflow (target path): `.github/workflows/ci.yml` — content currently staged at `.github/pending/ci.yml` until activated (`T-008`). **Status: not active — CI EXECUTION is NOT VERIFIED; zero runs exist.**

| Trigger | Jobs | Gate |
|---|---|---|
| Push (any branch) | `verify`, `shellcheck` | All checks must pass |
| Pull request | `verify`, `shellcheck` | All checks must pass |

- `verify` runs `bash scripts/verify/verify.sh` (structure, content, hygiene — see `scripts/verify/`).
- `shellcheck` lints every script in `scripts/verify/`.
- CI is intentionally dependency-free (no third-party actions beyond `actions/checkout`) so the gate itself stays auditable.

> **Bootstrap note (task `T-008`):** GitHub refuses to let automation tokens create files under `.github/workflows/` (it requires the `workflows` permission). Until a maintainer activates the workflow — move `.github/pending/ci.yml` to `.github/workflows/ci.yml` via the GitHub web UI — the workflow content lives staged in `.github/pending/`, and `verify_structure.sh` accepts that state **only while `T-008` is open** in `tasks/BACKLOG.md`.

### When CI is red

1. A red CI means the repository state contradicts its contract. Fixing it **takes precedence over new work**.
2. Reproduce locally: `bash scripts/verify/verify.sh` (or `shellcheck scripts/verify/*.sh`).
3. Fix the root cause; never weaken a check to make CI green. Weakening a check requires an explicit task and maintainer approval, recorded in `tasks/CURRENT.md`.

## Verification suite

- Entry point: `scripts/verify/verify.sh` — discovers and runs every `verify_*.sh` next to it.
- Current checks:
  - `verify_structure.sh` — required files exist and are non-empty.
  - `verify_content.sh` — governance content rules (state vocabulary, required sections, status-board discipline).
  - `verify_hygiene.sh` — no conflict markers, placeholders, trailing whitespace; final newlines.
- Adding a check: see `docs/DEVELOPMENT.md` → “Adding a verification check”.

## Releases and versioning

- Versions follow [Semantic Versioning](https://semver.org/); history is recorded in `CHANGELOG.md` (Keep a Changelog format).
- Cutting a release: update `CHANGELOG.md` (move `[Unreleased]` → `[x.y.z] — date`), tag `vx.y.z`, and record evidence in `tasks/CURRENT.md`.
- 0.x versions signal that the product purpose is still being defined.

## Repository maintenance

- **Branch protection on `main`** (backlog `T-003`): require PR, require CI pass, no direct pushes, no force pushes.
- **Labels:** `task`, `bug`, `enhancement`, `blocked` (used by the issue templates).
- **Secrets:** never committed; `.env*` is ignored. Rotation procedure if a secret leaks: revoke first, then purge history (which requires maintainer approval — history rewrites are forbidden to agents by `AGENTS.md` §4).
- **Backlog hygiene:** every completed backlog item must leave behind a row in `tasks/CURRENT.md` with its final state and evidence.

## Handoff operations

- Handoff records accumulate in `docs/HANDOFF.md` (newest first). They are never deleted; they are history.
- If `tasks/CURRENT.md` and a handoff record disagree, the files + commits win. Verify, fix the stale record, and note the correction in the new handoff.
