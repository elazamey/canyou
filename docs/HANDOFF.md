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

### 2026-08-31 20:45 UTC — T-000 — terminology refinement handoff

Agent:        Arena Agent (session-scoped; identity irrelevant to the contract)
Branch:       `arena/01a05905-canyou`
Base commit:  `73f8032` (state after the audit handoff)
Head commit:  `1f9eb6c` (vocabulary refinement) + the commit carrying this record

Done (state + evidence):
  - State vocabulary refined — COMMITTED — `1f9eb6c`: new `PREPARED` state
    (content not at its operational location); `IMPLEMENTED` tightened to
    require the operational location; `NOT INSTALLED` / `NOT VERIFIED`
    negations made first-class; rule added that a negation never satisfies
    its positive state (`AGENTS.md` §2, mirrored in `README.md`)
  - CI claims re-split to the precise model — COMMITTED — `tasks/CURRENT.md`:
    contract DOCUMENTED / content PREPARED / installation NOT INSTALLED
    (evidence: `git ls-files .github/workflows/` empty) / execution NOT
    VERIFIED (evidence: `gh pr checks 1` → “no checks reported”)
  - Checker hardened — VERIFIED — `verify_content.sh` validates exact state
    tokens; negative test passed (bogus `STAGED-READY` → FAIL naming the row;
    restore → full suite PASS; recorded in Verified Facts)

Not done / remaining (all maintainer-side; unchanged):
  - CI activation (`T-008`) → then record first green run link and raise
    CI installation/execution states with evidence
  - Merge of PR #1 into `main`
  - Q-1 (purpose of `canyou`) — blocks `T-001`/`T-002` and all application code

Decisions made this session:
  - Adopted the reviewer's terminology correction: the earlier PR-comment
    table row “CI FILE = IMPLEMENTED” is superseded by “CI WORKFLOW CONTENT =
    PREPARED / CI WORKFLOW = NOT INSTALLED”; a correction comment follows in
    PR #1 (corrections are appended, history is not edited)
  - An editing mistake in `tasks/CURRENT.md` (an unintended intermediate line)
    was immediately reverted before committing; working tree verified clean
    against `1f9eb6c` via `git diff` (empty)

Risks / open questions:
  - Status Board rows must now use exact state tokens (checker-enforced);
    free-text states will fail verification by design
  - Q-1/Q-2/Q-3 in `tasks/CURRENT.md` remain open for the maintainer

Immediate next step:
  - Maintainer only: activate CI (T-008), merge PR #1, answer Q-1. Agents:
    stop — no T-001, no stack, no application code before the purpose exists.

### 2026-08-31 20:10 UTC — T-000 — audit handoff (phase close-out)

Agent:        Arena Agent (session-scoped; identity irrelevant to the contract)
Branch:       `arena/01a05905-canyou`
Base commit:  `840477f` (state of PR #1 at review time)
Head commit:  `99ea878` (state fixes) + the commit carrying this record

Done (state + evidence):
  - PR #1 audited against the contract — VERIFIED — scope evidence:
    `git diff --name-only origin/main...HEAD` = 23 governance files, zero
    application code; `main` still at `e0b7fcf`; PR OPEN with commits
    `640ac83`, `840477f` (`gh pr view 1`)
  - CI state granularity enforced — COMMITTED — Status Board now splits
    CI into contract (DOCUMENTED) / file (IMPLEMENTED, staged) / execution
    (NOT VERIFIED); evidence: `gh pr checks 1` → “no checks reported”
  - 5 state-conflation points fixed — COMMITTED — `99ea878`: present-tense
    references to `.github/workflows/ci.yml` in `AGENTS.md` §5,
    `CHANGELOG.md`, `docs/ARCHITECTURE.md`, `docs/SECURITY.md`,
    `docs/OPERATIONS.md` reworded to staged/conditional (T-008)
  - Verification suite still passing — VERIFIED — `bash scripts/verify/verify.sh`
    → `RESULT: PASS — 3 check group(s)`, exit 0 (run before each audit commit)

Not done / remaining (all maintainer-side; no agent work authorized):
  - CI activation (`T-008`) — maintainer web-UI action, then record first green
    run link in `tasks/CURRENT.md` → Verified Facts
  - Merge of PR #1 into `main`
  - Q-1 (purpose of `canyou`) — blocks `T-001`/`T-002` and all application code

Decisions made this session:
  - Adopted finer CI granularity: CI CONTRACT = DOCUMENTED, CI FILE =
    IMPLEMENTED (staged), CI EXECUTION = NOT VERIFIED, LOCAL VERIFICATION =
    VERIFIED — recorded in the Status Board and Verified Facts
  - No workaround attempted for the GitHub `workflows`-permission constraint;
    staged-pending design kept as the honest interim state

Risks / open questions:
  - Until `T-008` closes, CI enforcement is manual (PR evidence); the strict
    gate returns automatically once the workflow file exists and `T-008` is
    marked DONE — if `T-008` is closed without activating, verification fails
  - Q-1/Q-2/Q-3 in `tasks/CURRENT.md` remain open for the maintainer

Immediate next step:
  - Maintainer only: activate CI (T-008), merge PR #1, answer Q-1. Agents: stop
    here — do not start T-001 and do not write application code.

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
