# Current Work State

> Single source of truth for **what is being worked on right now**. Maintained under the contract in [`AGENTS.md`](../AGENTS.md): read it before working, update it before finishing. States: `DOCUMENTED` → `PREPARED` → `IMPLEMENTED` → `VERIFIED` → `COMMITTED` (+ `HANDOFF_READY`; absence is recorded as `NOT INSTALLED` / `NOT VERIFIED`).

- **Last updated:** 2026-08-31 (UTC)
- **Active branch:** `arena/01a05905-canyou`
- **Head commit:** `640ac834aee669d819f7b6fc5a86b65ad75b2466`

## Active Task

**T-000 — Agent-Ready Repository Baseline: audited, ready to close pending merge + CI activation.** Governance layer complete except one-step CI activation (`T-008`). A contract audit of PR #1 (2026-08-31, commit `99ea878`) found and fixed 5 state-conflation points; no `VERIFIED` claim exists for CI execution. No application stack, no product code — deliberate. **Phase is closed from the agent side: T-001 is blocked until the maintainer defines the purpose of `canyou`.**

## Status Board

| Item | State | Evidence |
|---|---|---|
| Agent contract | COMMITTED | `AGENTS.md` @ `640ac83` |
| Work-state files | COMMITTED | `tasks/CURRENT.md`, `tasks/BACKLOG.md` @ `640ac83` |
| Continuation protocol | COMMITTED | `docs/HANDOFF.md` @ `640ac83` |
| Governance documentation | COMMITTED | `docs/ARCHITECTURE.md`, `docs/DEVELOPMENT.md`, `docs/OPERATIONS.md`, `docs/SECURITY.md` @ `640ac83` |
| Deterministic verification suite | COMMITTED | `scripts/verify/verify.sh` + 3 checks @ `640ac83` |
| CI contract (what CI must do) | DOCUMENTED | `docs/OPERATIONS.md` §Continuous Integration + `.github/pending/ci.yml` content |
| CI workflow content | PREPARED | `.github/pending/ci.yml` @ `640ac83` — staged; not at its operational location; activation is maintainer-only (`T-008`) |
| CI workflow installation | NOT INSTALLED | `.github/workflows/ci.yml` does not exist — evidence: `git ls-files .github/workflows/` → empty; `test ! -e .github/workflows/ci.yml` → true (2026-08-31) |
| CI execution | NOT VERIFIED | `gh pr checks 1` → “no checks reported” (2026-08-31); zero runs exist. Raise to `VERIFIED` only with a green run link |
| Collaboration templates | COMMITTED | `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md` @ `640ac83` |
| Repository meta files | COMMITTED | `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `LICENSE`, `.editorconfig`, `.gitignore` @ `640ac83` |

## Verified Facts

- **Verification suite passes on the baseline commit.**
  - Command: `bash scripts/verify/verify.sh`
  - Result (2026-08-31, on commit `640ac83` working tree): `RESULT: PASS — 3 check group(s). Repository state matches its contract.` — exit code 0; verify_content 12 checks PASS, verify_hygiene 4 checks PASS, verify_structure 18 PASS + 1 accepted-pending NOTE (CI staged, T-008).
- **`main` history before this work:** single commit `e0b7fcf` containing only a `README.md` stub — confirmed via `git log --oneline` and directory listing on 2026-08-31. Nothing else was ever implemented in this repository.
- **Push constraint (evidence):** `git push` of a commit containing `.github/workflows/ci.yml` was rejected by GitHub — `refusing to allow a GitHub App to create or update workflow .github/workflows/ci.yml without workflows permission`. Hence the staged-pending design and task `T-008`.
- **CI EXECUTION = NOT VERIFIED (audit, 2026-08-31):** `gh pr checks 1` → “no checks reported on the ‘arena/01a05905-canyou’ branch”. No CI run has ever executed in this repository; any CI claim above `DOCUMENTED` (contract) / `PREPARED` (content) is forbidden until a green run link is recorded here.
- **PR #1 scope audit (2026-08-31):** `git diff --name-only origin/main...HEAD` lists 23 governance files (markdown / yaml / bash / config) — zero application code, `main` still at `e0b7fcf` (verified via `git fetch` + `git log origin/main`).
- **CI WORKFLOW = NOT INSTALLED (evidence, 2026-08-31):** `git ls-files .github/workflows/` → empty output; `test ! -e .github/workflows/ci.yml` → true. The workflow content is PREPARED at `.github/pending/ci.yml` (tracked, verified via `git ls-files .github/pending/`).
- **State-vocabulary checker hardened + negative-tested (2026-08-31, on `1f9eb6c` tree):** `verify_content.sh` now validates the Status Board state cell by exact token (a negation can no longer satisfy a positive state via substring). Negative test: injecting the bogus token `STAGED-READY` made `verify_content.sh` FAIL (exit 1) naming the exact row; restoring the file made the full suite PASS again.

## Open Questions

- **Q-1:** What is the product purpose of `canyou`? (blocks `T-001`; maintainer decision)
- **Q-2:** Which application stack, if any? (blocks `T-002`; maintainer decision)
- **Q-3:** Documentation language(s) beyond English? (candidate backlog item `T-006`)

## Next Actions

1. Maintainer: activate CI per `T-008` — move `.github/pending/ci.yml` → `.github/workflows/ci.yml` via the GitHub web UI (on this branch or after merge), then delete the pending file and mark `T-008` DONE.
2. Maintainer: review and merge the baseline PR into `main`.
3. After the first CI run, record the run link here and raise “CI execution on GitHub” to `VERIFIED`.
4. Maintainer: answer Q-1 (what is `canyou`?), then start `T-001`. **No agent work is authorized before Q-1 is answered — no stack, no code.**
5. Any agent starting fresh: read `AGENTS.md` → this file → `docs/HANDOFF.md` (in that order).
