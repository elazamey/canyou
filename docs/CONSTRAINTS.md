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
| **Q-7 (owner directive, 2026-08-31)** | Requirements **SIGNED** — `docs/REQUIREMENTS.md` is the binding Requirements record; directive addendum recorded there (per-operation traceability §8, security contract §6, connector contract §7, slice composition §4-D/§5, free-first §9). |
| **PR #1 (owner directive, 2026-08-31)** | Merge **approved**; execution evidence recorded in `tasks/CURRENT.md`. |
| **Phase-1 slice (owner directive §4-D/§5, 2026-08-31)** | Minimal vertical slice **within (a)**: Tool Registry + Policy Gate + Connector Interface + one GitHub Connector + tests/permission boundaries + minimal per-execution evidence. GitHub selected as the first connector (R-3 deferral resolved for ADR-0001). No independent ledger, metering, memory, or multi-agent. |
| **P-3 (owner directive, 2026-08-31)** | Remains `PROPOSED/UNSIGNED`; never executable requirements without an independent owner decision. |

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

## Decision record (owner, 2026-09-01) — comprehensive plan: binding clauses — verbatim

**Source:** repository owner (elazamey), 2026-09-01, together with the master plan recorded in
`docs/ROADMAP.md`. Appended at the end of this file (append-only, `AGENTS.md` §4.9); the 2026-08-31
decision record above is untouched.
**Status:** signed by the owner as product strategy. The clauses below bind **how** later phases may be
executed; they do not create implementation scope by themselves (pipeline unchanged: `AGENTS.md` §2).

1. **Open core, paid convenience** — verbatim: «المنتج الأساسي مفتوح المصدر ومجاني، بينما ندفع المستخدم
   مقابل الراحة، الإدارة، التعاون، الأمان المؤسسي، والخدمات المتقدمة.»
2. **No financial barrier to run locally** — verbatim: «Canyou Core لا يفرض اشتراكًا أو حاجزًا ماليًا على
   المستخدم لتشغيل النسخة المحلية.» This is the approved external phrasing; «AI بالكامل مجاني» is
   explicitly **not** approved, because model cost may sit with an external provider and its quotas.
3. **Revenue never overrides the product philosophy** — verbatim: «لن نجعل الربح يتعارض مع فلسفة
   المنتج.» Engines: local free edition = adoption, Managed Cloud = revenue, Enterprise = high value,
   Marketplace = ecosystem, consulting = early revenue + feedback.
4. **Ordering is binding on agents** — verbatim: «Core → Trust → Users → Product → Revenue → Scale»,
   and the current priority «Security Gate → External Validation → Staging → Production Readiness».
5. **No pricing numbers before data** — verbatim: «التسعير يجب أن يُحدد بعد معرفة الاستخدام الحقيقي
   والتكاليف، وليس تثبيت أرقام مبكرة دون بيانات.» An agent may not invent plans, tiers, or prices.
6. **Self-healing is not autonomous merge** — verbatim: «Self-Healing لا تعني Autonomous Merge»:
   high-risk operations stay behind the Policy Gate and an owner authorization gate.
7. **The dashboard never gates local use** — the Web Arena is «مدخل SaaS لاحقًا، وليس شرطًا لتشغيل
   النسخة المحلية».
8. **No permanent grant dependency** — verbatim: «يُمنع أن تصبح الخطة المالية معتمدة على منحة أو رصيد
   مجاني دائم.»
9. **Exclusions in force now** (`docs/ROADMAP.md` §17): no early Marketplace, no Enterprise features
   before users, no SaaS before a stable core, no connector sprawl without real demand, no autonomous
   merge, no ungoverned self-healing, no costly cloud infrastructure before traction.
