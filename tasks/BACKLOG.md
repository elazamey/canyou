# Backlog

Queued work. Items move here → `tasks/CURRENT.md` **Active Task** when started. Backlog lifecycle: `OPEN` → `IN PROGRESS` (tracked in `tasks/CURRENT.md`) → `DONE` (leaves behind a status-board row with final state and evidence).

Nothing here is `IMPLEMENTED`. Backlog items are intentions, not claims about the repository.

## Backlog

| ID | Item | Status | Notes |
|---|---|---|---|
| T-001 | Define the product purpose and scope of `canyou` | DONE | Signed by owner 2026-08-31; recorded verbatim in `docs/PRODUCT.md` (see `tasks/CURRENT.md` → Verified Facts) |
| T-002 | Choose the application stack for the thin slice; record as an architecture decision in `docs/ARCHITECTURE.md` | OPEN | Owner decision; scoped to the thin slice (Tool Registry + Policy Gate + one Connector) |
| T-003 | Enable branch protection on `main` (require PR + passing CI, forbid force pushes) | OPEN | Repository settings; owner action on GitHub |
| T-004 | Adopt Architecture Decision Records (`docs/decisions/`) | OPEN | Do together with T-010 (first real technical decision) |
| T-005 | Cut the first release: version policy, tag `CHANGELOG.md` entries | OPEN | Only meaningful after the thin slice exists |
| T-006 | Decide documentation language policy (English-only vs bilingual) | OPEN | Currently English-only by convention (`CONTRIBUTING.md`) |
| T-007 | Add a markdown lint check to `scripts/verify/` if the docs grow | OPEN | Keep checks offline and deterministic |
| T-008 | Activate CI: move `.github/pending/ci.yml` → `.github/workflows/ci.yml` via the GitHub web UI, then delete the pending file | OPEN | One-step owner action; automation tokens lack the `workflows` permission GitHub requires to create workflow files |
| T-009 | Derive Requirements for the thin slice from `docs/PRODUCT.md` — every requirement carries owner/source | OPEN | Owner/architect step, or a delegated agent draft marked `DOCUMENTED` until owner signature (Q-4) |
| T-010 | ADR-001: thin-slice architecture — Tool → Policy → Execution → Connector → Provider chain; connectors hold no authority | OPEN | Blocked by T-009; pair with T-004 |
| T-011 | Thin-slice implementation: Tool Registry + Policy Gate + one Connector | OPEN | BLOCKED by T-009, T-010, T-002 — no application code before them |

## Ideas parking lot

- Template repository: reuse this baseline as a generator (`canyou init`) — do not start before T-001 is answered.
