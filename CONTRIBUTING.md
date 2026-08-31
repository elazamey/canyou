# Contributing to canyou

This repository is built to be worked on by **humans and autonomous agents side by side**. Both follow the same contract: [`AGENTS.md`](AGENTS.md). Read it before doing anything.

## The short version

1. **Read state first:** `tasks/CURRENT.md`, `tasks/BACKLOG.md`, `git status`.
2. **Bound your task:** goal, scope allowlist, out-of-scope list. Ask when ambiguous — do not invent requirements.
3. **Make the change** inside the scope allowlist only.
4. **Verify:** `bash scripts/verify/verify.sh` must pass. New behavior requires a new deterministic check.
5. **Document evidence:** update `tasks/CURRENT.md` (states + evidence) and append a handoff record to `docs/HANDOFF.md` if the session stops mid-task.
6. **Open a pull request** using `.github/pull_request_template.md`, including the exact verification command and its output.

## What we merge

- Changes that stay inside their declared scope.
- Changes whose claims are backed by evidence: `DOCUMENTED` < `IMPLEMENTED` < `VERIFIED` < `COMMITTED` (see `AGENTS.md` §2).
- Deterministic checks that fail loudly, not checks that always pass.

## What we do not merge

- Documentation that describes things that do not exist in the repository.
- Drive-by changes outside the task scope (split them into their own task instead).
- Anything containing secrets, credentials, or tokens.
- Agent-specific instructions injected into the neutral governance files.

## Style

- Follow `.editorconfig` (UTF-8, LF, final newline, no trailing whitespace).
- Write commit messages in Conventional Commit format (`feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`).
- Keep documentation in English so it stays agent-neutral and tool-friendly.

## Reporting problems

Open an issue using one of the templates in `.github/ISSUE_TEMPLATE/`. A bug without reproduction steps and evidence is a hypothesis, not a bug.
