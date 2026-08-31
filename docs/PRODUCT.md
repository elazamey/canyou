# Product Definition — canyou

> The single authoritative statement of what canyou **is**. Everything else derives from it through the pipeline below. Changes to this file require an explicit owner signature recorded in the file itself.

## Signed definition

Recorded **verbatim** (owner language: Arabic). Source: repository owner (elazamey), 2026-08-31.

> **«Canyou هو منصة تشغيل وكلاء (Agent Operating Platform)، وتبدأ المرحلة التنفيذية بشريحة رقيقة قابلة للتشغيل: Tool Registry + Policy Gate + Connector واحد.»**

English translation (convenience only — the Arabic text is authoritative):

> Canyou is an Agent Operating Platform, and the execution phase begins with a thin runnable slice: Tool Registry + Policy Gate + one Connector.

## What this definition fixes

1. **Product identity:** an operating platform for agents — Runtime + policy-governed Tools + evidence-backed execution + Provenance/Handoff, for humans and agents together *(identity clause source: owner, 2026-08-31)*.
2. **First execution scope:** exactly one thin slice — Tool Registry, Policy Gate, one Connector. Nothing else is in scope for the first implementation phase.
3. **The Connector is a native component inside the Runtime** (adapter/infrastructure layer), not a standalone project.
4. **The full platform vision is deliberately NOT recorded here.** The broader layer map discussed on 2026-08-31 remains owner draft material until it is derived and signed step by step through the pipeline. Nothing in conversation becomes a requirement by itself.

## Binding derivation pipeline

```text
Product Definition → Requirements → Architecture → Stack → Tasks →
Implementation → Verification → Evidence → Commit → Handoff
```

## Binding rules (source: owner, 2026-08-31)

1. **No requirement without an owner/source.**
2. **No implementation without a requirement.**
3. **No VERIFIED without evidence.**

## Current position in the pipeline

| Stage | State |
|---|---|
| Product Definition | DONE — this file |
| Requirements | NOT STARTED — owner/architect step (or an explicitly delegated draft awaiting owner signature) |
| Architecture | NOT STARTED — blocked by Requirements |
| Stack | NOT STARTED — owner decision (`T-002`), scoped to the thin slice |
| Implementation | BLOCKED — requires all of the above |
