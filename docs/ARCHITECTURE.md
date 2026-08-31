# Architecture

> Claims in this file are `DOCUMENTED` until proven otherwise. See `AGENTS.md` §2 for the state vocabulary and `tasks/CURRENT.md` for the current status board.

## Current reality

**This repository contains no application code.** It currently implements exactly one layer: the **agent governance layer** — the agent-ready baseline that makes the repository itself the carrier of work state, evidence, and continuation across agents.

No product purpose and no application stack have been chosen yet. When that decision is made, it will be recorded here as an architecture decision and mirrored in `tasks/CURRENT.md` and `tasks/BACKLOG.md`. Until then, no agent may assume a stack.

## Layer 1 — Governance layer (`IMPLEMENTED`)

The governance layer turns agent work into auditable repository state:

```
                 ┌──────────────────────────────────────────────┐
                 │            Any agent / human                 │
                 └────────────────────┬─────────────────────────┘
                                      │ 1. READ: contract + state
                                      ▼
   AGENTS.md (contract)   tasks/CURRENT.md (state)   tasks/BACKLOG.md (queue)
                                      │
                                      │ 2. EXECUTE inside scope allowlist
                                      ▼
                          Working tree (scoped change)
                                      │
                                      │ 3. VERIFY
                                      ▼
                      scripts/verify/verify.sh ── fail ──▶ fix before commit
                                      │ pass
                                      │ 4. COMMIT
                                      ▼
                           Git commit (evidence: SHA)
                                      │
                                      │ 5. UPDATE STATE + HANDOFF
                                      ▼
                     tasks/CURRENT.md  +  docs/HANDOFF.md
                                      │
                                      ▼
              the next agent resumes from repository state,
              never from another agent's conversation history
```

### Components

| Component | Path | Responsibility | State |
|---|---|---|---|
| Agent contract | `AGENTS.md` | Lifecycle, state vocabulary, hard rules | see `tasks/CURRENT.md` |
| Work state | `tasks/CURRENT.md` | Single source of truth for current work | see `tasks/CURRENT.md` |
| Work queue | `tasks/BACKLOG.md` | Planned, unstarted work | see `tasks/CURRENT.md` |
| Continuation protocol | `docs/HANDOFF.md` | Handoff records any agent can resume from | see `tasks/CURRENT.md` |
| Verification suite | `scripts/verify/` | Deterministic checks; single entry point `verify.sh` | see `tasks/CURRENT.md` |
| CI | `.github/workflows/ci.yml` | Runs verification + shellcheck on push/PR | see `tasks/CURRENT.md` |
| Collaboration interfaces | `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md` | Force scope + evidence at intake | see `tasks/CURRENT.md` |

The component table intentionally does **not** repeat states inline; `tasks/CURRENT.md` is the only place where states live, so there is exactly one state to keep truthful.

### Design rules for this layer

1. **One source of truth per concern:** work state lives only in `tasks/CURRENT.md`; handoff records only in `docs/HANDOFF.md`; verification only behind `scripts/verify/verify.sh`.
2. **Everything must run offline:** verification uses bash + coreutils only, no network, so any agent on any machine can reproduce it.
3. **Fail closed:** missing files, stale headings, or an unstatesed status row must fail verification, not pass silently.
4. **Agent-neutral:** governance files never reference a specific agent product or grant it special behavior.

## Layer 2 — Application layer (`DOCUMENTED` only — does not exist)

Intentionally empty. Filling it requires:

1. `T-001` — define the product purpose (maintainer decision),
2. `T-002` — choose the stack and record the decision here,
3. then implementation tasks in `tasks/BACKLOG.md`, each with its own verification commands.

## Extension rules

- New deterministic checks go into `scripts/verify/verify_*.sh` (auto-discovered by `verify.sh`).
- Architecture decisions change this file **and** the status board in `tasks/CURRENT.md` in the same commit.
- Any diagram or table here describes intent; the files on disk and the passing verification run are the truth.
