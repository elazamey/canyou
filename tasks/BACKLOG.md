# Backlog

Queued work. Items move here → `tasks/CURRENT.md` **Active Task** when started. Backlog lifecycle: `OPEN` → `IN PROGRESS` (tracked in `tasks/CURRENT.md`) → `DONE` (leaves behind a status-board row with final state and evidence).

Nothing here is `IMPLEMENTED`. Backlog items are intentions, not claims about the repository.

## Backlog

| ID | Item | Status | Notes |
|---|---|---|---|
| T-001 | Define the product purpose and scope of `canyou` | DONE | Signed by owner 2026-08-31; recorded verbatim in `docs/PRODUCT.md` (see `tasks/CURRENT.md` → Verified Facts) |
| T-002 | Choose the application stack for the thin slice; record as an architecture decision in `docs/ARCHITECTURE.md` | DONE | Decided in ADR-0001 (Python 3.11+, stdlib-only) per OWNER DIRECTIVE §4-C, 2026-08-31; TS-first rule inapplicable (no existing TS code) |
| T-003 | Enable branch protection on `main` (require PR + passing CI, forbid force pushes) | OPEN | Repository settings; owner action on GitHub — CI is live and green on main; recommended now that main carries the baseline |
| T-004 | Adopt Architecture Decision Records (`docs/decisions/`) | DONE | Mechanism adopted with ADR-0001 (2026-08-31); `verify_adr.sh` enforces form (negative-tested) |
| T-005 | Cut the first release: version policy, tag `CHANGELOG.md` entries | OPEN | Only meaningful after the thin slice exists |
| T-006 | Decide documentation language policy (English-only vs bilingual) | OPEN | Currently English-only by convention (`CONTRIBUTING.md`) |
| T-007 | Add a markdown lint check to `scripts/verify/` if the docs grow | OPEN | Keep checks offline and deterministic |
| T-008 | Activate CI: get `.github/workflows/ci.yml` onto GitHub, then delete the pending file | DONE | Closed 2026-08-31 with evidence: owner installed the workflow (`09b5090`); first runs failed on SC2164 only; fix `df777a3` (one line); green runs `33445296608`/`33445301389`; pending copy removed (`11178c5`, content-verified identical); post-deletion runs `33445781317`/`33445786957` green — all required jobs PASS (see `tasks/CURRENT.md` → Verified Facts) |
| T-009 | Derive Requirements for the thin slice from `docs/PRODUCT.md` — every requirement carries owner/source | DONE | Signed via OWNER DIRECTIVE Q-7 (2026-08-31) — `docs/REQUIREMENTS.md` is binding; directive addendum (§6/§7/§8/§9) appended with the signature |
| T-010 | ADR-0001: thin-slice architecture — Tool → Policy → Execution → Connector → Provider chain; connectors hold no authority | DONE | ADR-0001 ACCEPTED 2026-08-31 per OWNER DIRECTIVE §4-C (stack + layout + security/traceability shapes); Q-2 concluded |
| T-011 | Thin-slice implementation: Tool Registry + Policy Gate + one Connector | IN PROGRESS | Re-implemented from the documented specification in the working tree (2026-09-01): implemented + VERIFIED, **not committed** — commit pending owner review. Provenance: the original implementation commit (`241fb02f`) was LOST / EVIDENCE UNAVAILABLE with its ephemeral session; recovery search 2026-09-01 = NOT FOUND (7/7 sources negative); rebuilt from `docs/REQUIREMENTS.md` + ADR-0001 + directive §4-D/§5 only. AUTHORIZED by OWNER DIRECTIVE §4-D; §5 exclusions binding |

## Ideas parking lot

- Template repository: reuse this baseline as a generator (`canyou init`) — do not start before T-001 is answered.
