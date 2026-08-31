# Security

## Reporting a vulnerability

Use [GitHub private vulnerability reporting](https://github.com/elazamey/canyou/security/advisories/new)
(GitHub → Security → Report a vulnerability). Do **not** open a public issue for security problems.

Please include: the affected file(s)/path(s), reproduction steps, impact, and evidence. Reports without evidence are triaged last.

## Secrets policy

- No secrets, credentials, API keys, or tokens in the repository — including in tasks, handoff records, issue text, and verification output.
- `.env*` files are git-ignored; verification scripts never read secrets.
- If a secret leaks: revoke it **first**, then contact the maintainer. History purging requires maintainer approval; agents must never rewrite history themselves (`AGENTS.md` §4).

## Agent permission policy

Agents operating under `AGENTS.md`:

- must not rewrite history on `main` or force-push shared branches;
- must not exfiltrate repository contents or credentials to third parties;
- must not introduce third-party code or actions unless the task explicitly allows it;
- must stay inside the task's scope allowlist.

CI uses no third-party actions beyond `actions/checkout`, so the automated gate stays auditable.

## Current dependency posture

This repository has **no runtime dependencies and no application code** — only markdown and bash verification scripts. When an application stack is chosen (`T-002`), this section must be updated with a dependency policy and update/audit procedure in the same commit.

## Scope of this page

This page documents policy only (`DOCUMENTED`). Its enforcement points are: `AGENTS.md` (hard rules), `.github/workflows/ci.yml` (gate), and `.gitignore` (secret-shaped files). Anything not listed there is not enforced — treat it as intention, not mechanism.
