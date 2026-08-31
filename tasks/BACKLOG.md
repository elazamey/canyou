# Backlog

Queued work. Items move here → `tasks/CURRENT.md` **Active Task** when started. Backlog lifecycle: `OPEN` → `IN PROGRESS` (tracked in `tasks/CURRENT.md`) → `DONE` (leaves behind a status-board row with final state and evidence).

Nothing here is `IMPLEMENTED`. Backlog items are intentions, not claims about the repository.

## Backlog

| ID | Item | Status | Notes |
|---|---|---|---|
| T-001 | Define the product purpose and scope of `canyou` | DONE | Signed by owner 2026-08-31; recorded verbatim in `docs/PRODUCT.md` (see `tasks/CURRENT.md` → Verified Facts) |
| T-002 | Choose the application stack for the thin slice; record as an architecture decision in `docs/ARCHITECTURE.md` | OPEN | Owner decision; explicitly deferred until requirements are settled (Q-2, 2026-08-31); scoped to the thin slice |
| T-003 | Enable branch protection on `main` (require PR + passing CI, forbid force pushes) | OPEN | Repository settings; owner action on GitHub |
| T-004 | Adopt Architecture Decision Records (`docs/decisions/`) | OPEN | Do together with T-010 (first real technical decision) |
| T-005 | Cut the first release: version policy, tag `CHANGELOG.md` entries | OPEN | Only meaningful after the thin slice exists |
| T-006 | Decide documentation language policy (English-only vs bilingual) | OPEN | Currently English-only by convention (`CONTRIBUTING.md`) |
| T-007 | Add a markdown lint check to `scripts/verify/` if the docs grow | OPEN | Keep checks offline and deterministic |
| T-008 | Activate CI: get `.github/workflows/ci.yml` onto GitHub, then delete the pending file | DONE | Closed 2026-08-31 with evidence: owner installed the workflow (`09b5090`); first runs failed on SC2164 only; fix `df777a3` (one line); green runs `33445296608`/`33445301389`; pending copy removed (`11178c5`, content-verified identical); post-deletion runs `33445781317`/`33445786957` green — all required jobs PASS (see `tasks/CURRENT.md` → Verified Facts) |
| T-009 | Derive Requirements for the thin slice from `docs/PRODUCT.md` — every requirement carries owner/source | IN PROGRESS | Owner delegated the draft (Q-4, 2026-08-31): `docs/REQUIREMENTS.md` produced as DOCUMENTED (R-1..R-7, sourced to signed material only); awaiting owner signature |
| T-010 | ADR-001: thin-slice architecture — Tool → Policy → Execution → Connector → Provider chain; connectors hold no authority | OPEN | Blocked by T-009 signature; scope formulation (a) reaffirmed by owner (Q-6); pair with T-004 |
| T-011 | Thin-slice implementation: Tool Registry + Policy Gate + one Connector | OPEN | BLOCKED by T-009 (signed), T-010, T-002 — no application code before them; scope creep forbidden (owner, 2026-08-31) |

## Ideas parking lot

- Template repository: reuse this baseline as a generator (`canyou init`) — do not start before T-001 is answered.
