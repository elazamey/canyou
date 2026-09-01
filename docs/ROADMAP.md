# Master Plan — Product, Governance, Launch, and Profitability

Owner's own title, verbatim: **خطة Canyou الشاملة — المنتج، الحوكمة، الإطلاق، والربحية**

> Authoritative record of **what canyou is going to become, in which order, and on what commercial
> terms**. Work state lives in `tasks/CURRENT.md`; scope admission lives in `docs/REQUIREMENTS.md` +
> the pipeline in `AGENTS.md` §2. This file sequences them; it does not replace any of them.

- **Source:** repository owner (elazamey), 2026-09-01 — delivered as a directive message; recorded here.
- **Status:** `SIGNED` by the owner as the system master plan (product strategy + phase order + revenue model).
- **Fidelity note:** the text below is preserved verbatim, including the Arabic prose, the section
  numbering, and the ASCII diagrams. Two mechanical accommodations are disclosed here rather than hidden:
  (1) heading depth (the plan's `#`/`##` became `##`/`###`) so the file stays well-formed under its own
  title; (2) the plan's H1 title is rendered in English above and its Arabic original is kept verbatim
  immediately below it. No wording, ordering, or number inside the plan was altered, added, or removed.
- **Language:** Arabic original is authoritative (same convention as `docs/PRODUCT.md`).

## Governing effect — what this record changes and what it does not

1. **Phase-1 scope is unchanged.** The signed thin slice (Tool Registry + Policy Gate + one Connector,
   `docs/PRODUCT.md` + `docs/REQUIREMENTS.md`) remains the only implementable scope. This plan does not
   expand it, and `MERGED ≠ RELEASED`: the slice is merged on `main`, not deployed.
2. **Nothing in this plan is `IMPLEMENTED`.** Every phase at or after Phase 2 is `DOCUMENTED` in this
   file only. A phase becomes implementable only through the pipeline: requirements row → ADR →
   backlog/task → implementation → deterministic verification → evidence → commit → handoff
   (`AGENTS.md` §2, §3). Architectural choices named here (Arena orchestration, self-healing loop,
   hosted control plane, marketplace) each require their own ADR before code.
3. **It settles sequencing, and it outranks the unsigned proposals.** `docs/PROPOSALS.md` §P-2 and §P-3
   stay `UNSIGNED` background. Where they disagree with this plan about order or priority, **this record
   governs**; where they agree (Arena and governance as the product's identity, not a bolt-on), the
   owner's own words are now in this file and the proposals add nothing binding.
4. **The zero-financial-barrier rule is a product constraint, not marketing copy.** §15 is recorded in
   `docs/CONSTRAINTS.md` alongside the signed nine rules; §17's exclusions are recorded as stop-rules.
5. **Monetization is sequenced after trust.** No pricing number is fixed here, on purpose: pricing is a
   data-driven decision (`tasks/CURRENT.md` → Open Questions) and any future Entitlement/Billing work
   needs its own requirements + ADR (the signed "monetization-ready without gating function" rule).

## The plan (verbatim, owner, 2026-09-01)

## 1. الرؤية

Canyou ليس مجرد AI Agent يكتب كودًا، بل منصة **Agentic Engineering** تجمع بين:

**Multi-Agent Arena + Connectors + Policy Governance + Evidence + CI/CD + Local-First Execution**

والفكرة التجارية الأساسية:

> **المنتج الأساسي مفتوح المصدر ومجاني، بينما ندفع المستخدم مقابل الراحة، الإدارة، التعاون، الأمان المؤسسي، والخدمات المتقدمة.**

---

## 2. المرحلة الحالية — تثبيت النواة والحوكمة

هذه هي المرحلة التي وصل إليها المشروع فعليًا، ويجب استكمالها قبل التوسع في الميزات.

### النواة

* Tool/Connector Registry
* Policy Gate
* Default DENY
* Connector isolation
* Evidence / Trace
* Fail-Closed behavior
* Offline testing
* GitHub integration
* Verification framework
* Agent execution boundaries

### الحوكمة

* Protected `main`
* Pull Request workflow
* Required CI checks
* Security Gates
* Provenance
* Current state / Backlog / Handoff
* Evidence-driven release process

### الهدف

الوصول إلى:

**Secure Core + Reproducible + Auditable + Testable**

---

## 3. المرحلة التالية — Security & External Validation

بعد اكتمال دورة T-011/T-003:

### Security Gate

اختبار:

* Authentication
* Authorization
* Least Privilege
* Secrets handling
* Connector isolation
* Policy bypass resistance
* Evidence integrity
* Network failure
* Timeout handling
* Error handling

### External Validation

إثبات أن:

```text
Registry
→ Policy
→ Connector
→ Transport
→ Evidence
```

يعمل على خدمة خارجية حقيقية، وليس فقط Fake/Offline transport.

### Staging

ثم:

```text
Security
→ External
→ Staging
→ Smoke Tests
→ Production Readiness
```

---

## 4. المنتج الأساسي — Open Source / Local First

بعد استقرار النواة، يكون المنتج الأساسي مجانيًا.

### النسخة المجانية

* تشغيل محلي
* CLI
* Local Agent Runtime
* Connectors
* Policy Engine
* Verification
* Local Evidence
* دعم النماذج المحلية
* دعم APIs المجانية عندما تكون متاحة
* إمكانية استخدام مفاتيح المستخدم مباشرة

### المبدأ

> **لا يحتاج المستخدم إلى اشتراك مدفوع كي يبدأ باستخدام Canyou.**

وهذا يصبح عنصر جذب أساسي.

---

## 5. Multi-Agent Arena — الميزة التنافسية الرئيسية

يصبح لدى Canyou وضع Arena يمكن فيه تنفيذ نفس المهمة بواسطة أكثر من Agent/Model.

مثال:

```text
                    TASK
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       Agent A    Agent B    Agent C
       Gemini     Local LLM   Other
          │          │          │
          ▼          ▼          ▼
       Branch A   Branch B   Branch C
          │          │          │
          └──────────┼──────────┘
                     ▼
                   CI
                     ▼
             Tests / Quality
                     ▼
               Arena Score
                     ▼
              Owner Decision
```

المقارنة لا تعتمد على "من كتب كودًا أجمل"، بل على أدلة قابلة للقياس مثل:

* Test pass rate
* Correctness
* Regression count
* Execution time
* Cost where measurable
* Reliability
* Policy compliance

وهذا يجعل **Arena** جزءًا من هوية المنتج وليس مجرد ميزة إضافية.

---

## 6. Self-Healing Agent Loop

بعد استقرار الـRuntime، نبني حلقة تنفيذ ذاتية محكومة:

```text
Task / Issue
    ↓
Planner
    ↓
Multiple Agents
    ↓
Branches
    ↓
CI
    ↓
Failure Analysis
    ↓
Repair Attempt
    ↓
Re-test
    ↓
Evidence
    ↓
Owner Gate
```

لكن:

> **Self-Healing لا تعني Autonomous Merge.**

تبقى العمليات عالية الخطورة خلف Policy وOwner Authorization.

---

## 7. Web Arena Dashboard

بعد استقرار CLI/Runtime:

### لوحة Web

تعرض:

* Active Tasks
* Agents
* Model selection
* Branches
* PRs
* CI status
* Test scores
* Evidence
* Policy decisions
* Execution history
* Arena comparison

والواجهة تصبح **مدخل SaaS لاحقًا**، وليس شرطًا لتشغيل النسخة المحلية.

---

## 8. النموذج التجاري — Open Core

نحن لا نبيع المحرك الأساسي أولًا.

نبيع:

> **Managed Experience + Team Features + Enterprise Controls**

### الطبقة الأولى — Free / Open Source

```text
Canyou Core
$0
```

تشمل:

* Local Runtime
* CLI
* Connectors الأساسية
* Policy
* Evidence
* Arena الأساسية
* Local Models
* BYOK

---

## 9. Hosted Managed Cloud — أول مصدر إيراد رئيسي

المستخدم الذي لا يريد إدارة البنية التحتية يدفع مقابل الراحة.

### Managed Cloud

يوفر:

* تشغيل مستضاف
* Dashboard
* Agent orchestration
* إدارة Jobs
* نتائج Arena
* CI integration
* Persistent workspace
* Team collaboration
* Managed connectors
* Usage analytics

الفكرة:

```text
Open Source
   ↓
User can self-host for $0

OR

Managed Cloud
   ↓
Pay for convenience
```

التسعير يجب أن يُحدد بعد معرفة الاستخدام الحقيقي والتكاليف، وليس تثبيت أرقام مبكرة دون بيانات.

---

## 10. Enterprise

عندما يبدأ الاستخدام المؤسسي، نضيف:

### Enterprise Controls

* RBAC
* SSO
* Advanced audit logs
* Organization policies
* Approval workflows
* Private deployments
* Advanced secrets management
* Compliance tooling
* Centralized governance
* Dedicated support
* Custom connectors
* SLA / operational support

الفكرة:

> المؤسسة لا تشتري "AI" فقط؛ تشتري **Control + Governance + Security + Support**.

---

## 11. Agent & Connector Marketplace

بعد وجود قاعدة مستخدمين:

```text
Canyou Marketplace
│
├── Agents
├── Connectors
├── Policies
├── Workflows
└── Extensions
```

يمكن للمطورين نشر:

* Agents متخصصة
* GitHub/GitLab connectors
* Cloud connectors
* DevOps tools
* QA agents
* Security agents
* Domain workflows

ويأخذ Canyou نسبة من المبيعات أو الاشتراكات.

---

## 12. Consulting & Custom Engineering

هذه ستكون غالبًا أول قناة إيراد عملية قبل الوصول إلى SaaS واسع النطاق.

نستخدم Canyou نفسه كـPortfolio حي لبناء:

* Custom Agent Systems
* Internal Developer Platforms
* AI automation
* Private agent infrastructure
* Connector development
* Governance systems
* Enterprise AI integration

وهكذا يصبح:

```text
Canyou
   ↓
Proof of capability
   ↓
Consulting
   ↓
Customers
   ↓
Feedback
   ↓
Product improvement
```

---

## 13. Sponsorships / Grants / Credits

قناة مساندة وليست الأساس:

* GitHub Sponsors
* Open Collective
* Open-source grants
* Cloud credits
* AI API credits
* Developer programs

ويُمنع أن تصبح الخطة المالية معتمدة على منحة أو رصيد مجاني دائم.

---

## 14. استراتيجية اكتساب المستخدمين

### المرحلة الأولى

**Authority**

نطلق:

* GitHub
* Documentation
* CLI
* Demo
* Examples
* Benchmarks
* Security model
* Arena demonstrations

الهدف:

> الثقة أولًا.

### المرحلة الثانية

**Community**

* Early adopters
* Contributors
* Connector developers
* Agent creators

### المرحلة الثالثة

**Managed Cloud**

نحوّل المستخدم الذي يريد الراحة إلى عميل مدفوع.

### المرحلة الرابعة

**Enterprise**

نحوّل الشركات التي تحتاج Governance وSecurity وSupport إلى عقود أعلى قيمة.

---

## 15. استراتيجية Zero Financial Barrier

الميزة التي سنحافظ عليها:

```text
Local
= $0 possible

Self-hosted
= $0 possible

BYOK
= user controls provider cost

Managed Cloud
= paid convenience
```

لكن لا نقول:

> "AI بالكامل مجاني"

لأن تكلفة نماذج الذكاء الاصطناعي قد تعتمد على مزود خارجي وحصصه وأسعاره.

الرسالة الأدق:

> **Canyou Core لا يفرض اشتراكًا أو حاجزًا ماليًا على المستخدم لتشغيل النسخة المحلية.**

---

## 16. الترتيب التنفيذي النهائي

```text
PHASE 1
Core Runtime
+
Governance
+
Connectors
        ↓
PHASE 2
Security
+
External Validation
+
Staging
        ↓
PHASE 3
Open Source CLI
+
Local Agent Runtime
        ↓
PHASE 4
Multi-Agent Arena
+
Benchmarking
        ↓
PHASE 5
Web Arena Dashboard
        ↓
PHASE 6
Managed Cloud
        ↓
PHASE 7
Marketplace
        ↓
PHASE 8
Enterprise
        ↓
PHASE 9
Consulting / Custom Solutions
        ↓
PHASE 10
Scale
```

---

## 17. ما الذي لا أفعله الآن؟

لن أشتت النظام بـ:

* Marketplace مبكرًا
* Enterprise features قبل وجود مستخدمين
* SaaS قبل استقرار Core
* عشرات Connectors بلا طلب حقيقي
* Autonomous Merge
* Self-Healing غير محكوم
* بنية سحابية مكلفة قبل وجود traction

الترتيب:

> **Core → Trust → Users → Product → Revenue → Scale**

---

## 18. الهدف التجاري النهائي

نريد أن يصبح Canyou بهذا النموذج:

```text
             CANYOU
                │
     ┌──────────┼───────────┐
     ▼          ▼           ▼
 Open Source   Cloud      Enterprise
     │          │           │
     ▼          ▼           ▼
 Community   Revenue     High-value
     │          │          contracts
     └──────────┼───────────┘
                ▼
          Marketplace
                │
                ▼
          Larger Ecosystem
```

والحلقة التجارية:

```text
Free Core
   ↓
Adoption
   ↓
Trust
   ↓
Teams
   ↓
Cloud
   ↓
Enterprise
   ↓
Marketplace
   ↓
Ecosystem
```

## القرار الاستراتيجي

**لن نجعل الربح يتعارض مع فلسفة المنتج.**

النسخة المحلية المجانية هي **محرك الانتشار**، والـManaged Cloud هو **محرك الإيراد**، والـEnterprise هو **محرك القيمة العالية**، والـMarketplace هو **محرك النظام البيئي**، والاستشارات هي **محرك الإيراد المبكر والتغذية الراجعة**.

أما الآن، فالأولوية لا تزال:

**Security Gate → External Validation → Staging → Production Readiness.**

بهذا تصبح استراتيجية الربح جزءًا من خارطة النظام نفسها، لا مشروعًا منفصلًا يظهر بعد اكتمال التقنية.

## Phase → repository reality (the honest state of each phase)

States follow `AGENTS.md` §2. This table is deliberately unflattering: a phase is worth what its
evidence is worth.

| Phase | Content | State in the repository | Gate that must close before it can move |
|---|---|---|---|
| 1 | Core Runtime + Governance + Connectors | `COMMITTED` / `MERGED` (T-011 slice on `main` @ `6f35c05`); governance layer `IMPLEMENTED`; branch protection `OPEN` (`T-003`) | Owner's `T-003` protection + release cut (`T-005`) stay separate decisions |
| 2 | Security + External Validation + Staging + Smoke + Production Readiness | `DOCUMENTED` here; `NOT STARTED` | Owner authorization to open the Security Gate; then `T-012` → `T-014` |
| 3 | Open Source CLI + Local Agent Runtime (free tier as a product surface) | `DOCUMENTED`; `NOT STARTED` | License/packaging/CLA decision (`T-022`), requirements + ADR |
| 4 | Multi-Agent Arena + Benchmarking | `DOCUMENTED`; `NOT STARTED` | ADR (orchestration + scoring), requirements; scoring must be evidence-based, not aesthetic |
| 5 | Web Arena Dashboard | `DOCUMENTED`; `NOT STARTED` | ADR (web stack — ADR-0001's stdlib-only rule binds the core, not a future web tier); it must not become a prerequisite for local use |
| 6 | Managed Cloud (first revenue engine) | `DOCUMENTED`; `NOT STARTED` | Cost/usage data (§9: no numbers without data), separate ADR + security review |
| 7 | Marketplace | `DOCUMENTED`; `NOT STARTED` | User base first (§17 forbids this early) |
| 8 | Enterprise controls | `DOCUMENTED`; `NOT STARTED` | Enterprise users first (§17) |
| 9 | Consulting / custom solutions | `DOCUMENTED`; not a repository work item | Recorded as a revenue/feedback channel only; nothing here licenses client work |
| 10 | Scale | `DOCUMENTED`; `NOT STARTED` | Sequel to all of the above |

### Standing exclusions from §17 (recorded as stop-rules for agents)

No marketplace work, no enterprise features, no SaaS infrastructure, no connector sprawl, **no
autonomous merge**, and **no self-healing loop without a policy gate and an owner gate**. An agent that
believes it needs any of these now is misreading this file: record the reason in `tasks/CURRENT.md`
instead of building it.

### Commercial posture as an engineering constraint (from §15)

`Canyou Core` may never acquire a hard dependency that turns the local-first path into a paid one. That
is an acceptance criterion for future phases (it inherits the signed "free-first, no credit card" rule in
`docs/CONSTRAINTS.md`), and the wording of §15 — "no subscription or financial barrier to run the local
version", never "AI is free" — is the only approved external phrasing.
