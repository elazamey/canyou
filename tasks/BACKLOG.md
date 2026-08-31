# Backlog

Queued work. Items move here → `tasks/CURRENT.md` **Active Task** when started. Backlog lifecycle: `OPEN` → `IN PROGRESS` (tracked in `tasks/CURRENT.md`) → `DONE` (leaves behind a status-board row with final state and evidence).

Nothing here is `IMPLEMENTED`. Backlog items are intentions, not claims about the repository.

## Backlog

| ID | Item | Status | Notes |
|---|---|---|---|
| T-001 | Define the product purpose and scope of `canyou` | OPEN | Maintainer decision; everything else depends on it |
| T-002 | Choose the application stack; record as an architecture decision in `docs/ARCHITECTURE.md` | OPEN | Blocked by T-001; no stack may be assumed before this |
| T-003 | Enable branch protection on `main` (require PR + passing CI, forbid force pushes) | OPEN | Repository settings; owner action on GitHub |
| T-004 | Adopt Architecture Decision Records (`docs/decisions/`) | OPEN | Do together with the first real technical decision |
| T-005 | Cut the first release: version policy, tag `CHANGELOG.md` entries | OPEN | Only meaningful after T-001 |
| T-006 | Decide documentation language policy (English-only vs bilingual) | OPEN | Currently English-only by convention (`CONTRIBUTING.md`) |
| T-007 | Add a markdown lint check to `scripts/verify/` if the docs grow | OPEN | Keep checks offline and deterministic |
| T-008 | Activate CI: move `.github/pending/ci.yml` → `.github/workflows/ci.yml` via the GitHub web UI, then delete the pending file | OPEN | One-step maintainer action; automation tokens lack the `workflows` permission GitHub requires to create workflow files |

## Ideas parking lot

- Template repository: reuse this baseline as a generator (`canyou init`) — do not start before T-001 is answered.
