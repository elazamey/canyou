# Project Constraints — Binding

> **Binding project constraints.** Signed by the repository owner on 2026-08-31. Every requirement, architecture decision, and task in this repository must satisfy them or explicitly declare a deferral that does not violate them. Changes require a new owner signature recorded in this file.

## Decision record (owner, 2026-08-31) — verbatim

> «Q-5 كامل مع تحسين الهوية من P-2 كتحسين مرشّح فقط دون أن يغيّر التعريف الموقّع، Q-6 الصياغة (a) الموقّعة، Q-4 فوّضك بمسودة DOCUMENTED حتى توقيعي، Q-2 نناقشه بعد تثبيت المتطلبات، والقديم الثابت T-008 → أول تشغيل CI أخضر → دمج PR #1. لا ترقية للنطاق ولا كود خارج ذلك قبل تثبيت المتطلبات.»

Dispositions recorded from that signature:

| Decision | Disposition |
|---|---|
| **Q-5** | P-1 constraint package signed **in full** (rules + six areas below) → binding. P-2 §5 identity statement endorsed as a **refinement candidate only** — it does not amend the signed definition in `docs/PRODUCT.md`. Everything else in P-2 remains unsigned (`docs/PROPOSALS.md`). |
| **Q-6** | Phase-1 scope formulation **(a) — the signed one — reaffirmed**: «Tool Registry + Policy Gate + Connector واحد». Formulations (b) (P-1 §4) and (c) (P-2 §6 `v0`) are **not adopted**. `docs/PRODUCT.md` is unchanged. |
| **Q-4** | Owner delegates the Requirements draft to the agent: produced as `DOCUMENTED` (`docs/REQUIREMENTS.md`) until the owner signs it. |
| **Q-2** | Stack discussion explicitly deferred until requirements are settled. |

## The nine rules (source: owner channel 2026-08-31; signed Q-5)

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

## The six constraint areas (source: owner channel 2026-08-31; signed Q-5)

1. **No model training** — models are providers only behind a Model Router (Gemini / Hugging Face / Local / future); swapping a model must not change the Agent Runtime.
2. **Free-first, no credit card** — core runtime, core development, and core deployment must run free; no fatal dependency on card-required platforms even when a free tier exists; paid services optional only.
3. **Free API keys via Model Router + Provider Adapters** — quota, rate limit, fallback, provider health, cost policy; keys never leak to the agent/model.
4. **Monetization-ready without gating function** — Usage Meter → Entitlement Engine → Plans → future Billing Provider; MVP launches free; monetization added later without re-engineering the Runtime.
5. **Ownership evidence as core architecture** — every significant artifact carries content hash, creator, timestamp, parent artifact, repository, commit, execution id, agent id, tool calls, provenance chain. (Owner-channel caveat retained: the technical record helps prove creation and sequence but is not by itself a substitute for legal IP procedures or registration where required.)
6. **Agent = Untrusted Actor** — Policy → Permission → Tool → Connector → External Service; secrets isolated from the model; least-privilege tools; audited actions; approval gates for sensitive actions; sandboxed connectors where possible; hashed artifacts; immutable execution ledger.

## Applying the constraints to Phase 1 (scope formulation (a))

The signed Phase-1 slice (Tool Registry + Policy Gate + one Connector) must **obey** every constraint while **not expanding** to fully implement the ones that describe the whole platform. Specifically:

- Areas 1 and 3 (Model Router, provider adapters) — **not part of the slice** (it contains no model integration); the slice must not preclude them.
- Area 4 (monetization) — **not part of the slice**; the slice must not preclude metering later.
- Area 5 and the ledger clause of area 6 — the **Execution Ledger is deliberately out of the slice** (owner, Q-6: no scope creep). The slice carries only the minimal auditable decision record emitted by the Policy Gate (area 6 “actions → audited”), which is a property of the Gate, not a new component.
- Areas 2 and 6 (free-to-run, untrusted actor, policy-before-execution) — **fully binding on the slice** from day one.
