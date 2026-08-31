# AGENTS.md — Agent Operating Contract

This file is the **operating contract for any autonomous agent working in this repository** — Claude Code, Codex, Cursor, Arena, Copilot coding agent, or any other. It is deliberately *agent-neutral*: it defines no agent-specific behavior, privilege, or identity, and no agent may add agent-specific instructions to it.

Operating on this repository means accepting this contract. If you cannot comply, stop and write a handoff (`docs/HANDOFF.md`).

## 1. Prime directive — the repository is the single source of truth

- No agent owns work state. **The repository is the single source of truth.**
- Conversation history, agent memory, and context are **not** evidence.
- Any agent must be able to answer, from the repository alone: *what happened, what remains, and what is the proof?*
- If a fact is not recorded in a file and fixed by a commit, it does not exist.

## 2. State vocabulary

Every claim about something in this repository must carry exactly one of these states:

| State | Meaning | Required evidence |
|---|---|---|
| `DOCUMENTED` | Described in documentation only | File path + heading |
| `PREPARED` | Content exists in the repository but **not at its operational location** (e.g., a CI workflow staged under `.github/pending/` instead of `.github/workflows/`) | Path to the staged content |
| `IMPLEMENTED` | Actually present in the repository files **at its operational location** — for activation-gated artifacts (workflows, configs), staged content is `PREPARED`, not `IMPLEMENTED` | Path(s) to the implementation |
| `VERIFIED` | Passed a deterministic, reproducible check | Exact command + observed output |
| `COMMITTED` | Fixed in Git history | Commit SHA |
| `HANDOFF_READY` | Another agent can safely resume from where work stopped | Handoff record in `docs/HANDOFF.md` |

Rules:

- **Documentation is never proof of implementation.** A feature described in `README.md` or `docs/ARCHITECTURE.md` may not exist in code at all. Always check the files.
- `VERIFIED` requires a reproducible command, not an assertion or an impression.
- States may only be raised with new evidence, and must be lowered when evidence turns out to be stale.
- **A negation never satisfies a positive state.** The status board may record absence first-class using `NOT INSTALLED` / `NOT VERIFIED`; these never count as their positive counterparts (`NOT VERIFIED` is not `VERIFIED`; `PREPARED` is not `IMPLEMENTED`).

## 3. Work lifecycle — mandatory order

Work proceeds in this exact order. Skipping a step invalidates the session.

```
READ → UNDERSTAND → EXECUTE → VERIFY → DOCUMENT EVIDENCE → COMMIT → UPDATE STATE → HANDOFF
```

### 3.1 READ — load the real state, not assumptions

1. Read `tasks/CURRENT.md` (current work state).
2. Read `tasks/BACKLOG.md` (queued work).
3. Run `git status`, `git branch --show-current`, and `git log --oneline -10`.
4. Read the latest handoff record in `docs/HANDOFF.md`, if any.
5. Treat all documentation as claims to verify, not as facts.

### 3.2 UNDERSTAND — bound the task

1. Identify the task and its acceptance criteria (issue, backlog item, or `tasks/CURRENT.md` entry).
2. Write down: the goal, the **scope allowlist** (paths that may change), and the out-of-scope list.
3. If the task is ambiguous, stop and ask the maintainer. **Do not invent requirements.**

### 3.3 EXECUTE

1. Change only what the task requires. No drive-by refactors, no reformatting of unrelated files.
2. Follow the conventions in `CONTRIBUTING.md` and `docs/DEVELOPMENT.md`.
3. Do not add an application stack or product code unless the task explicitly asks for it.

### 3.4 VERIFY

1. Run `bash scripts/verify/verify.sh`. It must pass.
2. If the change introduces new behavior, add or extend a deterministic check in `scripts/verify/`. A change is not `VERIFIED` until a reproducible check exists.
3. Capture the exact command(s) and their output for the evidence step.

### 3.5 DOCUMENT EVIDENCE

Record in `tasks/CURRENT.md` (and the PR description): what changed, its state, and the evidence (command + output; commit SHA once known).

### 3.6 COMMIT

1. Commit using Conventional Commit messages (`feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`), scoped to the task.
2. One logical change per commit. The verification suite must pass at every commit.

### 3.7 UPDATE STATE

Update `tasks/CURRENT.md`: move finished items forward (`IMPLEMENTED` → `VERIFIED` → `COMMITTED`), refresh Verified Facts, Open Questions, and Next Actions to match reality.

### 3.8 HANDOFF

Append a handoff record to `docs/HANDOFF.md` (use its template) so any other agent can continue without access to this session's conversation.

## 4. Hard rules

1. **Do not invent requirements.** Unstated does not mean intended.
2. **Do not modify outside the task scope.** If a fix outside scope seems necessary, record it in `tasks/BACKLOG.md` instead of doing it.
3. **Do not exceed permissions.** Never rewrite history on `main`, never force-push shared branches, never touch secrets or credentials, never introduce third-party code unless the task explicitly allows it.
4. **Do not treat documentation as proof of implementation.**
5. **Do not skip verification.** No verify, no commit.
6. **Do not leave state stale.** Every session ends with `tasks/CURRENT.md` matching reality.
7. **Do not fake completion.** If the task cannot be finished, write an honest handoff stating exactly what remains.
8. **Keep governance agent-neutral.** No agent-specific instructions, names, or behavior in `AGENTS.md`, `docs/`, or `tasks/`.

## 5. Verification contract

- `scripts/verify/verify.sh` is the single deterministic entry point; once activated (`.github/workflows/ci.yml`, staged pending `T-008` — see `docs/OPERATIONS.md`), CI runs it on every push and pull request. Until activation, the accepted verification evidence in pull requests is the locally captured command + output.
- Checks are plain `bash` + coreutils, require no network, and exit non-zero on any failure.
- A red CI means the repository state contradicts its contract. Fixing it takes precedence over new work.

## 6. Repository map

| Path | Role | Maintained by |
|---|---|---|
| `AGENTS.md` | This operating contract | Maintainer |
| `tasks/CURRENT.md` | Current work state — read first, updated last | Every agent session |
| `tasks/BACKLOG.md` | Queued work | Agents + maintainer |
| `docs/HANDOFF.md` | Continuation protocol + handoff records | Every agent session |
| `docs/*.md` | Architecture, development, operations, security | Contributors |
| `scripts/verify/` | Deterministic verification suite | Contributors |
| `.github/` | CI, issue templates, pull request template | Maintainer |

## 7. Current reality check

This repository currently contains **only the agent governance layer**. No product purpose, application stack, or application code has been chosen yet. Do not assume one. Check `tasks/CURRENT.md` and `tasks/BACKLOG.md` for what is actually being worked on.
