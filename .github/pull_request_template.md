<!--
Pull requests follow AGENTS.md. A PR without verification evidence is not
reviewable and will not be merged. Documentation is not proof of implementation.
-->

## Summary

<!-- What does this change do, and why? -->

Task ID (from tasks/BACKLOG.md, tasks/CURRENT.md, or an issue):

## State impact

- [ ] `tasks/CURRENT.md` updated (Status Board / Verified Facts / Open Questions / Next Actions)
- [ ] Handoff record appended to `docs/HANDOFF.md` (required if work spans sessions or is incomplete)

<!-- Optional: old state → new state for the affected items. -->

## Verification evidence

<!-- Paste the exact command and the observed output. "It works" is not evidence. -->

Command:

```text
bash scripts/verify/verify.sh
```

Output:

```text
<paste the relevant output here>
```

## Scope confirmation

- [ ] Changes stay inside the declared task scope (no drive-by changes)
- [ ] No secrets, credentials, or tokens introduced
- [ ] Documentation describes only what actually exists in this PR (`DOCUMENTED` ≠ `IMPLEMENTED`)
- [ ] No agent-specific instructions added to governance files
