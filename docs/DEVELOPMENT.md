# Development

How to work on this repository — for humans and agents. The binding contract is [`AGENTS.md`](../AGENTS.md); this page is the practical manual.

## Prerequisites

- `git`
- `bash` (the verification suite is plain bash + coreutils; no network required)
- No other tooling is needed until an application stack is chosen (`T-002`).

## Setup

```bash
git clone https://github.com/elazamey/canyou.git
cd canyou
bash scripts/verify/verify.sh
```

If the last command does not pass, the checkout contradicts the repository contract — stop and fix that before any new work.

## The workflow in practice

1. **Read state**
   ```bash
   git status
   git branch --show-current
   git log --oneline -10
   ```
   Then read `tasks/CURRENT.md`, `tasks/BACKLOG.md`, and the latest record in `docs/HANDOFF.md`.

2. **Bound the task.** Write the goal, the scope allowlist (paths you may touch), and the out-of-scope list. If anything is ambiguous, ask — do not invent requirements.

3. **Branch naming**
   ```text
   task/T-003-branch-protection     (human/agent task branch, references a backlog ID)
   ```

4. **Make the change** inside the allowlist only.

5. **Verify**
   ```bash
   bash scripts/verify/verify.sh
   ```
   Capture the command and output — this is your evidence. If you added behavior, add a check in `scripts/verify/verify_*.sh` so the behavior becomes `VERIFIED`, not just `IMPLEMENTED`.

6. **Commit** (Conventional Commits, one logical change per commit)
   ```bash
   git commit -m "chore: add branch-protection notes to operations docs"
   ```

7. **Update state.** Move items forward in `tasks/CURRENT.md` (`IMPLEMENTED` → `VERIFIED` → `COMMITTED` with the commit SHA), refresh Open Questions and Next Actions.

8. **Handoff.** Append a record to `docs/HANDOFF.md` if the session is ending or the task is incomplete.

## Editing append-only records (`AGENTS.md` §4 rule 9)

When inserting a new proposal into `docs/PROPOSALS.md`, a handoff record into `docs/HANDOFF.md`, or content into any governing record:

1. Locate the **end** of the latest existing section and insert **after** it — never select-and-replace an existing heading or block.
2. Before committing, print the structure and eyeball it:
   ```bash
   grep -n '^## \|^### ' docs/PROPOSALS.md   # or docs/HANDOFF.md
   ```
   Confirm: the previous section is complete (same subsection count as before your edit) and your section follows it.
3. Run `bash scripts/verify/verify_records.sh` — it enforces anchors (exact subsection counts for registered entries) plus the floor for new entries.
4. When appending a **new** P-entry: register its subsection count in the `ANCHORS` table inside `scripts/verify/verify_records.sh` (same commit).
5. If you discover a loss: restore immediately, and disclose the slip in the handoff record. Never commit over a silent loss.

This procedure exists because insertion-replacement slips happened three times on 2026-08-31 (all caught and fixed pre-commit) — the rule turns that lesson into mechanics.

## Adding a verification check

1. Create `scripts/verify/verify_<topic>.sh` (it is auto-discovered by `verify.sh`).
2. Follow the existing style: `set -uo pipefail`, print `PASS <topic>: …` / `FAIL <topic>: …`, exit non-zero on any failure.
3. Keep it deterministic and offline. No timestamps, no randomness, no network in the pass/fail logic.
4. Run the full suite and commit the check together with the behavior it verifies.

## Style

- `.editorconfig` is authoritative: UTF-8, LF, final newline, no trailing whitespace.
- Markdown uses 2-space indentation; keep lines readable (~120 characters max).
- Documentation in English (agent-neutral). Anything described in docs but not present in files must be labeled `DOCUMENTED` in `tasks/CURRENT.md`.

## Before you finish (checklist)

- [ ] `bash scripts/verify/verify.sh` passes, output captured.
- [ ] No changes outside the scope allowlist.
- [ ] `tasks/CURRENT.md` reflects reality (states + evidence).
- [ ] Handoff record appended if the session ends mid-task.
- [ ] Commit message follows Conventional Commits.
