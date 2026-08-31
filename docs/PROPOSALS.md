# Proposals — Unsigned Inputs Awaiting Owner Signature

> **Intake log.** Nothing in this file is a requirement, constraint, or architecture decision. Material here arrived through the owner channel but is **not signed**; per `AGENTS.md` §2 (no requirement without an owner/source; conversation content is never by itself a requirement), it cannot govern work until the owner signs it. Signed items leave this file and move to their authoritative home (`docs/PRODUCT.md`, requirements records, or ADRs) with source and date. This file is history — entries are never edited or deleted, only superseded by a signature recorded elsewhere.

## P-1 — 2026-08-31 — Platform constraints package — `PROPOSED` / `UNSIGNED`

**Source:** advisor-voice message conveyed through the owner channel, 2026-08-31 (verbatim closer: «وسأتعامل معها كقيود دائمة للمشروع في المحادثات القادمة» — a statement of the *proposer's* intent, not an owner signature).
**Status:** awaiting owner decisions Q-5 (constraint signature) and Q-6 (Phase-1 scope amendment) in `tasks/CURRENT.md`.
**Effect if signed:** becomes binding project constraints and amends/extends the signed definition in `docs/PRODUCT.md`.

### 1. Proposed binding rule set (verbatim, owner channel)

```text
FREE TO BUILD
FREE TO RUN
FREE TO DEPLOY
NO CREDIT CARD
NO MODEL TRAINING
PROVIDER AGNOSTIC
SECURITY FIRST
PROVENANCE BY DEFAULT
MONETIZATION READY
```

### 2. Proposed constraint areas (six)

1. **No model training** — models are providers only behind a Model Router (Gemini / Hugging Face / Local / future); swapping a model must not change the Agent Runtime.
2. **Free-first, no credit card** — core runtime, core development, and core deployment must run free; no fatal dependency on card-required platforms even when a free tier exists; paid services optional only.
3. **Free API keys via Model Router + Provider Adapters** — quota, rate limit, fallback, provider health, cost policy; keys never leak to the agent/model.
4. **Monetization-ready without gating function** — Usage Meter → Entitlement Engine → Plans → future Billing Provider (FREE / PRO / TEAM sketch); MVP launches free, monetization added without re-engineering the Runtime.
5. **Ownership evidence as core architecture** — every significant artifact carries: content hash, creator, timestamp, parent artifact, repository, commit, execution id, agent id, tool calls, provenance chain. *(Proposer's own caveat, kept verbatim in spirit: the technical record helps prove creation and sequence but is not by itself a substitute for legal IP procedures or registration where required.)*
6. **Agent = Untrusted Actor** — Policy → Permission → Tool → Connector → External Service; secrets isolated from the model; least-privilege tools; audited actions; approval gates for sensitive actions; sandboxed connectors where possible; hashed artifacts; immutable execution ledger.

### 3. Proposed five pillars

```text
1. Agent Runtime        (Planning / Execution / State / Handoff)
2. Governed Tools       (Tool Registry / Policy Engine / Connector System / Approval Gates)
3. Evidence & Provenance (Execution Ledger / Hashes / Artifact Provenance / Version History / Ownership Evidence)
4. Free AI Provider Layer (Gemini / Hugging Face / Local / Provider Fallback & Routing)
5. Security & Monetization (Secrets Isolation / RBAC / Audit / Tenant Isolation / Usage & Billing architecture)
```

### 4. Proposed Phase-1 slice — ⚠️ AMENDMENT of a signed record

```text
Tool Registry + Policy Gate + Connector Interface + GitHub Connector + Execution Ledger + Security Boundary
```

The **signed** definition (`docs/PRODUCT.md`, owner, 2026-08-31) fixes the first execution slice as: «Tool Registry + Policy Gate + Connector واحد». The proposal above is a **superset** (adds Connector Interface as an explicit component, names GitHub as the connector, adds Execution Ledger and Security Boundary). It may supersede the signed scope **only** through an explicit owner-signed amendment recorded in `docs/PRODUCT.md`.

### 5. Proposed framing

"Governed Connector Framework": Canyou Agent → Tool Registry → Policy Gate → Connector Runtime → GitHub/Vercel/Cloudflare/… → Evidence → Provenance Ledger. The connector is explicitly **not** a bare API wrapper and holds no authority (policy precedes execution).
