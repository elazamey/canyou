# Proposals — Unsigned Inputs Awaiting Owner Signature

> **Intake log.** Nothing in this file is a requirement, constraint, or architecture decision. Material here arrived through the owner channel but is **not signed**; per `AGENTS.md` §2 (no requirement without an owner/source; conversation content is never by itself a requirement), it cannot govern work until the owner signs it. Signed items leave this file and move to their authoritative home (`docs/PRODUCT.md`, requirements records, or ADRs) with source and date. This file is history — entries are never edited or deleted, only superseded by a signature recorded elsewhere.

## P-1 — 2026-08-31 — Platform constraints package — `PROPOSED` / `UNSIGNED`

**Source:** advisor-voice message conveyed through the owner channel, 2026-08-31 (verbatim closer: «وسأتعامل معها كقيود دائمة للمشروع في المحادثات القادمة» — a statement of the *proposer's* intent, not an owner signature).
**Status:** awaiting owner decisions Q-5 (constraint signature) and Q-6 (Phase-1 scope amendment) in `tasks/CURRENT.md`.
**Update 2026-08-31 (owner signature Q-5):** signed **in full** — promoted to the binding record `docs/CONSTRAINTS.md`. This entry remains as intake history.
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

## P-2 — 2026-08-31 — Strategic positioning package — `PROPOSED` / `UNSIGNED`

**Source:** advisor-voice message conveyed through the owner channel, 2026-08-31 (verbatim markers: «حكمي النهائي», «أرى», «في رأيي»).
**Status:** awaiting owner decisions (carried Q-5/Q-6/Q-4 in `tasks/CURRENT.md`).
**Update 2026-08-31 (owner decisions Q-5/Q-6):** §5 identity statement endorsed by the owner as a **refinement candidate only** (no amendment to `docs/PRODUCT.md`); **all other sections remain unsigned**. Phase-1 scope formulation (a) was reaffirmed — this package’s `v0` (§6) is **not adopted**. See `docs/CONSTRAINTS.md` §Decision record.
**Relationship to P-1:** elaborates P-1 constraints (provider-agnostic, no model training) into a competitive thesis; introduces a version roadmap whose `v0` is a **third formulation of the Phase-1 scope** (see §6 warning).

### 1. Core thesis (verbatim)

> «لا تنافسهم في "ذكاء النموذج" فقط؛ نافسهم في "ذكاء النظام الذي يستخدم النموذج".»

Closing framing (verbatim):

```text
Claude  = Intelligence Engine
Manus   = Agent Product
Canyou  = Governed Agent Operating Platform
```

Goal statement (verbatim): «اجعل Canyou ينفّذ المهمة بصورة أكثر موثوقية، قابلية للتحقق، أمانًا، قابلية للامتداد، وأقل اعتمادًا على مزود واحد.»

### 2. Explicit non-goal

No competition on model intelligence / model size / general capability (consistent with P-1 §1 “NO MODEL TRAINING”). Realistic claim: Canyou can beat them **in specific bounded use-cases** (e.g., full software-project management idea → PR → deployment with evidence ledger, permission constraints, provenance), judged on *system outcome*, not model IQ.

### 3. Differentiation areas (summarized from the proposer’s table)

Real competitive fields: long-task execution, provenance (as a core feature, not theirs), governance, multi-provider AI, unified GitHub/deploy workflow, tailored memory, human+agent handoff, free/no-card, self-host/local, ownership evidence. Fields explicitly conceded: model size, reasoning strength.

### 4. Distributed intelligence (proposed architecture principle)

```text
Goal → Planner → Model Router → Specialist Agents → Tool Registry → Policy Gate
→ Execution → Verification → Evidence → Provenance → Handoff
```

Step-level model selection (“ما النموذج الأنسب لهذه الخطوة؟” — Planning→A, Coding→B, Summarization→C, Vision→D, Local/private→E). Capability formula (verbatim):

```text
Effective Agent Capability = Model Intelligence × Tools × Context × Memory ×
Orchestration × Verification × Permissions × Persistence
```

### 5. Candidate identity statement (verbatim — refinement candidate only)

> «Canyou ليس Chatbot. Canyou هو Operating System لوكلاء AI يعملون تحت سيطرة الإنسان، ويتركون سجلًا قابلاً للتحقق لكل ما فعلوا.»

Consistent with the signed definition (`docs/PRODUCT.md`); recorded here as an unsigned refinement candidate.

### 6. Version roadmap (verbatim) — ⚠️ third Phase-1 scope formulation

```text
v0 = Agent Runtime + Tool Registry + Policy Gate + 1 Connector + Execution Ledger
v1 = + GitHub + Vercel + Memory + Verification
v2 = + Multi-agent + Provenance + Handoff + Model Router
v3 = + SaaS + Teams + Monetization + Marketplace
```

**Warning:** `v0` differs from both the **signed** Phase-1 scope («Tool Registry + Policy Gate + Connector واحد», `docs/PRODUCT.md`) and the P-1 §4 superset (which adds Connector Interface, GitHub Connector, Security Boundary but not an explicit Agent Runtime). Three formulations now exist; exactly one can be current — resolving this is the owner’s Q-6 decision, recorded as an amendment in `docs/PRODUCT.md`.

### 7. Proposed next step (pipeline-gated)

“Canyou Competitive Architecture” document. Note: under `AGENTS.md` §2 this derives from **signed** constraints/requirements — it cannot be produced from conversation material until Q-5/Q-6 (and then T-009/T-010) are settled.

## P-3 — 2026-08-31 — Hypothetical owner-decision package — `PROPOSED` / `UNSIGNED`

**Source:** advisor-voice message via the owner channel, 2026-08-31. **Explicitly hypothetical framing (verbatim):** «لو كنت أنا مالك Canyou» / «لو كان القرار بيدي الآن» — decision *recommendations*, not an owner signature. Nothing below is executed or binding.
**Status:** awaiting the owner’s real decisions on the standing gates (Q-7, PR #1 merge, later Q-2).
**Update 2026-08-31 (advisor ruling, explicitly not an owner signature):** P-3 remains `PROPOSED/UNSIGNED`; recommended disposition — adopt only the non-conflicting subset (system-intelligence thesis; free-first as platform capability; provider-agnostic; least-privilege; GitHub-connector as ADR candidate); provenance/metering fields require signed requirements amendments; the 0–5 phase plan is strategy only; **no PR merge on this basis**. Executive reference stays Q-6 = formulation (a).

### 1. Recommended dispositions (hypothetical)

Q-5/Q-6 restated as already signed (no change). Q-7: sign after review. PR #1: merge. Q-2 preference rule (verbatim): «TypeScript إذا كان الـrepo الحالي TypeScript؛ وإلا Python للـruntime المستقل» — note: the repository currently contains **no application code in any language**, so under that rule the pointer would be Python; entirely unsigned.

### 2. Restated non-negotiable principles (subset of the signed CONSTRAINTS; one reframe)

The 7-rule list repeats signed material. **Reframe worth noting (verbatim):** «لا أجعل "مجاني" وعدًا مطلقًا تجاه خدمات خارجية قد تغيّر شروطها؛ بل أجعل Canyou نفسه قادرًا على العمل بدون خدمة مدفوعة إلزامية» — a narrower, more defensible reading of FREE-FIRST (platform capability, not a promise about third parties). Candidate refinement of `docs/CONSTRAINTS.md` if signed.

### 3. Phase plan (0–5) — candidate roadmap

PHASE 0 Governance+CI (done) → PHASE 1 Tool Registry + Policy Gate + GitHub Connector («first real Agent execution») → PHASE 2 Ledger + Provenance + Memory + Verification → PHASE 3 Vercel/Cloudflare + Model Router → PHASE 4 Multi-agent + Handoff → PHASE 5 Monetization/Teams/Marketplace. Consistent with P-2 §6 ordering; still unsigned.

### 4. Nominations and designs (candidates, unsigned)

- **GitHub as the first connector** — rationale: exercises Read/Write/Branch/Commit/PR/Permission/Audit/Error-handling. Input for ADR-001 (`T-010`), not a requirement (R-3 deliberately names no provider).
- **Chain contract** Agent → Tool Registry → Policy Gate → Connector Runtime → Provider API → Evidence; agent never sees secrets (`github.create_pull_request` instead of handing over `GITHUB_TOKEN`). Already the signed shape (R-2/R-4, CONSTRAINTS area 6) — restated.
- **Risk taxonomy per tool** (github.read_file LOW … merge_pr HIGH, delete_repo BLOCKED) — candidate Policy Gate design for `T-010`.
- **Provenance fields from day one:** execution_id, agent_id, tool_id, timestamp, input_hash, output_hash, artifact_hash, policy_decision.
- **Commercial architecture from day one:** Usage Meter, Entitlements, Plans, Limits, Tenant ID (payment excluded from MVP).
- **Model Router only, no model building** — restates signed area 1; Runtime stays model-agnostic.
- **Competition framing** («أول انتصار حقيقي… Agent نفّذ عملية حقيقية على GitHub تحت Policy وسجّل الدليل كاملًا») and the Practical Agent Quality formula — strategy context, unsigned.

### 5. ⚠️ Tensions with signed records (must be reconciled if ever signed)

1. **Provenance fields (§4) vs R-5:** the signed-scope Requirements draft deliberately keeps a *minimal* Gate decision record and excludes an Execution Ledger component (owner’s own Q-6 anti-scope-creep ruling). Adopting §4’s field set in Phase 1 would expand R-5 — requires a signed requirements amendment, not silent adoption.
2. **Usage Meter/Entitlements/Tenant ID (§4) vs R-7 and CONSTRAINTS §Applying:** monetization/metering is an explicit Phase-1 **non-goal**; the binding obligation is “not precluded”, not “built”. Building it now would amend R-7.
3. **GitHub Connector (§4) vs R-3:** requirements name no provider by design; the nomination belongs in ADR-001 after Q-7.

These tensions are exactly why intake ≠ promotion: each adoption path runs through the pipeline (Requirements → Architecture → Stack → Tasks).

