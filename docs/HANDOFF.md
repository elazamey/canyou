# Handoff — Continuation Protocol

This file makes work **transferable between agents and humans without conversation history**. The repository, not any agent's memory, carries the state (`AGENTS.md` §1).

## When a handoff is required

- At the end of any working session (agent or human).
- Immediately when stopping mid-task, for any reason (timeout, interruption, blocker).
- Whenever a task changes owner.

## Record template

Copy this template verbatim and fill every field. Do not omit “Not done” — an empty remainder list is a claim that nothing remains.

```text
### <YYYY-MM-DD HH:MM UTC> — <task ID or "no-task"> — handoff

Agent:        <name/type, optional — neutrality is fine>
Branch:       <branch>
Base commit:  <SHA this session started from>
Head commit:  <SHA of this session's last commit, or "none">

Done (state + evidence):
  - <item> — <DOCUMENTED|IMPLEMENTED|VERIFIED|COMMITTED|HANDOFF_READY> — <evidence>

Not done / remaining:
  - <item> — <why it stopped here, and the concrete next step>

Decisions made this session:
  - <decision> — <reason>

Risks / open questions:
  - <risk or question>

Immediate next step:
  - <one action the receiving agent can take without asking anyone>
```

## Rules for the writing agent

1. Be honest and specific. “Almost done” is meaningless — say exactly what remains.
2. Link evidence: file paths, commands + output, commit SHAs.
3. Append the record at the top of **Latest handoff records** below (newest first). Never delete or edit older records.
4. A handoff complements `tasks/CURRENT.md`; it does not replace updating it.

## Rules for the receiving agent

1. Read `tasks/CURRENT.md` first, then the newest record below.
2. If a handoff record and the repository disagree, **the files and commits win**. Re-verify, fix the stale record, and note the correction in your own handoff.
3. Re-run `bash scripts/verify/verify.sh` before starting work.
4. Verify every inherited claim before building on it (`AGENTS.md` §2: documentation is not proof).
5. Re-bound the task scope yourself (`AGENTS.md` §3.2) — do not inherit scope blindly.

## Latest handoff records

### 2026-08-31 19:30 UTC — T-000 — handoff

Agent:        Arena Agent (session-scoped; identity irrelevant to the contract)
Branch:       `arena/01a05905-canyou`
Base commit:  `e0b7fcf` (Initial commit — README stub only)
Head commit:  `640ac834aee669d819f7b6fc5a86b65ad75b2466` (this record is in the commit after it)

Done (state + evidence):
  - Governance layer: contract, state files, handoff protocol, docs, verification
    suite, collaboration templates — COMMITTED — commit `640ac83`
  - Verification suite passing — VERIFIED — `bash scripts/verify/verify.sh`
    → `RESULT: PASS — 3 check group(s)`, exit 0 (details in `tasks/CURRENT.md`)
  - CI workflow content — IMPLEMENTED as a file, staged — `.github/pending/ci.yml`

Not done / remaining:
  - CI activation (`T-008`) — GitHub rejected the automated push of
    `.github/workflows/ci.yml` (`workflows` permission); a maintainer must move
    `.github/pending/ci.yml` → `.github/workflows/ci.yml` via the web UI
  - Merge of the baseline PR into `main` — awaiting maintainer review
  - First CI run evidence — record the run link in `tasks/CURRENT.md` after activation
  - Product purpose (`T-001`) and stack decision (`T-002`) — blocked on Q-1/Q-2

Decisions made this session:
  - Governance files English-only and agent-neutral (no Arena-specific rules inside `AGENTS.md`)
  - License MIT; changelog Keep a Changelog + SemVer; commits Conventional Commits
  - No application stack chosen — deliberate, deferred to `T-002`
  - Branch history was rewritten locally once, before the first successful push:
    local-only commits `e5b08d5`/`3da3557` (which included the workflow file) were
    superseded by `640ac83` + this commit after the push rejection. No shared
    history was rewritten; evidence in `tasks/CURRENT.md` → Verified Facts.

Risks / open questions:
  - `verify_hygiene.sh` placeholder scan excludes `scripts/` so check scripts may
    mention the patterns they enforce (documented in the script header)
  - CI `shellcheck` job installs shellcheck via apt only if missing — confirm on first run
  - While `T-008` is open, `verify_structure.sh` accepts the staged-pending CI state;
    closing `T-008` without activating the workflow will correctly fail verification

Immediate next step:
  - Maintainer: activate CI per `T-008` (web UI: add `.github/workflows/ci.yml`
    with the content of `.github/pending/ci.yml`), then watch the first CI run and
    record it in `tasks/CURRENT.md` → Verified Facts.
