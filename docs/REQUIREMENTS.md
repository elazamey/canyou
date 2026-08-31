# Requirements — Phase 1 Thin Slice (SIGNED)

> **Status: SIGNED — binding Requirements record.** Signed via OWNER DIRECTIVE (Q-7 = SIGNED), 2026-08-31 — see the signature block and `docs/CONSTRAINTS.md` §Decision record. Originally a delegated agent draft (owner decision Q-4, 2026-08-31) derived **exclusively** from signed material: `docs/PRODUCT.md` (signed definition) and `docs/CONSTRAINTS.md` (signed constraints). Nothing in `docs/PROPOSALS.md` sources a requirement. The owner directive addendum (2026-08-31) below extends — never narrows — R-1..R-7.

**Slice scope (signed, formulation (a)):** Tool Registry + Policy Gate + one Connector. Non-goals are explicit in R-7.

## Traceability summary

| Req | Statement (one line) | Source |
|---|---|---|
| R-1 | Tools are registered with declared contracts and discoverable | `docs/PRODUCT.md` (slice), `docs/CONSTRAINTS.md` area 6 |
| R-2 | Every tool invocation passes the Policy Gate before execution; default is DENY | `docs/CONSTRAINTS.md` area 6, rules (SECURITY FIRST) |
| R-3 | Exactly one connector exists, as an adapter that holds no authority | `docs/PRODUCT.md` (slice, “native component / adapter layer”) |
| R-4 | Connectors are reachable only through Tool → Policy; never directly | `docs/CONSTRAINTS.md` area 6 |
| R-5 | The Gate emits an auditable decision record per invocation attempt | `docs/CONSTRAINTS.md` area 6 (“actions → audited”), rule (PROVENANCE BY DEFAULT) |
| R-6 | The slice builds, runs, and verifies with zero paid services and no card | `docs/CONSTRAINTS.md` area 2, rules (FREE TO BUILD/RUN/DEPLOY, NO CREDIT CARD) |
| R-7 | Explicit non-goals protect the slice from scope creep | Owner decision Q-6 (2026-08-31), `docs/PRODUCT.md` |

## Requirements

### R-1 — Tool Registry with declared contracts

The platform provides a registry where a tool is registered with a declared contract: stable name, description of the operation, and the permissions/capabilities it requires. Registered tools are discoverable by name and enumerable. Referencing an unregistered tool is a well-defined NOT_FOUND outcome, never an undefined behavior.

- Source: `docs/PRODUCT.md` (slice: “Tool Registry”); `docs/CONSTRAINTS.md` area 6 (least-privilege tools require declared permissions).
- Acceptance: deterministic check — register a tool; look it up by name (found, contract returned); enumerate (present); look up an unknown name (NOT_FOUND, no crash).

### R-2 — Policy Gate before every execution; default DENY

No tool execution may occur without a policy decision rendered first. The decision is ALLOW or DENY with a machine-readable reason. When no policy rule matches, the outcome is DENY (secure default). A capability that exists (tool registered, connector able) may still be blocked by policy — existence never implies permission.

- Source: `docs/CONSTRAINTS.md` area 6 (Agent = Untrusted Actor; Policy → Permission → Tool → Connector) and rule SECURITY FIRST.
- Acceptance: deterministic check — invoke an allowed tool (executed); invoke a tool with a DENY policy (blocked, reason recorded); invoke with no matching policy rule (DENY).

### R-3 — Exactly one connector, an adapter holding no authority

The slice contains exactly one connector, implemented as an adapter/infrastructure component inside the Runtime (not a standalone project). The connector executes requests that already passed the Policy Gate and performs no authorization decisions of its own. Which provider the adapter targets is an **architecture** decision (task `T-010`), not a requirement — the signed scope names no provider.

- Source: `docs/PRODUCT.md` (slice: “Connector واحد”; “native component inside the Runtime, adapter/infrastructure layer, not a standalone project”).
- Acceptance: deterministic check — the slice exposes exactly one connector implementation; direct invocation bypassing the Gate is impossible through public interfaces (verified by attempting the bypass and asserting it is rejected).

### R-4 — No path around the Gate

Connectors are reachable only via the Tool → Policy path. Neither the agent nor any caller can reach a connector directly. There is no privileged internal route that skips the policy decision.

- Source: `docs/CONSTRAINTS.md` area 6 (chain Policy → Permission → Tool → Connector → External Service; connectors hold no authority).
- Acceptance: deterministic check — the only public entry to connector functionality is through the gated tool path; a bypass attempt fails by design.

### R-5 — Auditable Gate decision record (minimal)

For every invocation attempt, the Gate emits a record containing: tool name, decision (ALLOW/DENY), reason, and a timestamp. Records are append-only within a run. This is the minimal “actions → audited” property of the Gate itself — **not** an Execution Ledger component, which is deliberately out of the slice (owner decision Q-6).

- Source: `docs/CONSTRAINTS.md` area 6 (“actions → audited”), rule PROVENANCE BY DEFAULT (minimal, non-component application inside the slice).
- Acceptance: deterministic check — after the R-2 scenarios, exactly one record per attempt exists with the four required fields; records cannot be modified through public interfaces.

### R-6 — Free to build, run, and verify

The slice must build, run, and pass its verification with zero paid services, zero credit-card requirements, and no network dependency for its deterministic checks. Any future paid integration is optional and must not be required for the slice to function.

- Source: `docs/CONSTRAINTS.md` area 2 and rules FREE TO BUILD / FREE TO RUN / FREE TO DEPLOY / NO CREDIT CARD.
- Acceptance: deterministic check — the full verification suite runs offline; CI (once activated) runs on free runners.

### R-7 — Explicit non-goals of the slice

Out of scope for Phase 1 (each is platform future, not slice work): model integration / Model Router / provider adapters; multi-agent orchestration; Execution Ledger as a component; memory; UI; monetization/metering; additional connectors; approval workflows beyond the DENY default; self-host packaging. These exclusions protect the slice from scope creep (owner decision Q-6, 2026-08-31) and must be re-scoped only through signed requirements.

- Source: owner decision Q-6 (recorded in `docs/CONSTRAINTS.md` §Decision record); `docs/PRODUCT.md` (slice formulation (a)).
- Acceptance: deterministic check — the slice’s public surface introduces none of the excluded components (structural review against the slice definition).

## Constraint compliance note

Areas 1, 3, 4 and the ledger clause of 6 (`docs/CONSTRAINTS.md`) are **deferred-by-design** for the slice and obeyed by not being precluded; areas 2 and 6 are fully binding now (see `docs/CONSTRAINTS.md` §Applying the constraints to Phase 1).

## Owner directive addendum (2026-08-31)

> Signed with Q-7 via the OWNER DIRECTIVE («التصنيف: OWNER DECISION — الحالة: ACTIVE»). Each item extends its requirement; requirement minima remain binding within the supersets.

1. **Per-operation traceability (directive §8)** — every operation executed by the slice emits a trace record carrying at minimum: `execution_id`, `agent_id`, `tool_id`, `timestamp`, `policy_decision`, input/output evidence reference, and artifact reference where applicable. Superset of R-5 (its four mandatory fields remain required within it). Deliberately **not** an independent Execution Ledger system.
2. **Security contract (directive §6)** — every tool declares: identity, permissions, risk level, approval requirement, audit information. Destructive operations (merge/delete/destructive) are never granted as default permissions. Extends R-1/R-2.
3. **Connector contract (directive §7)** — approved chain: Agent → Tool Registry → Policy Gate → Connector Runtime → GitHub API → Evidence. **GitHub is the first connector** (owner selection — resolves R-3’s deliberately deferred provider choice for ADR-0001).
4. **Phase-1 slice composition (directive §4-D, §5)** — within scope (a): Tool Registry, Policy Gate, Connector Interface, one GitHub Connector, tests and permission boundaries, minimal per-execution evidence. Directive §5 exclusions reinforce R-7 (no Vercel/Cloudflare/extra connectors, no multi-agent, no advanced memory, no metering/billing implementation, no marketplace, no training, no independent full ledger, no scope expansion).
5. **Free-first architecture (directive §9)** — never select a service merely for a “free tier”; Canyou Core must not stop working because an external service became paid; provider abstraction is mandatory; Gemini/Hugging Face/local models are providers, never the heart of the system. Consistent with constraint areas 1–3 (deferred-by-design for the slice, not precluded).

## Signature block (SIGNED)

- Owner signature: **elazamey (sayed_elazamy)** — via OWNER DIRECTIVE, Q-7 = SIGNED («القرار أدناه ملزم للتنفيذ، ولا يحتاج إلى إعادة طلب موافقة على كل خطوة داخله»)
- Date: 2026-08-31
- Effect upon signing: **executed** — this file is the binding Requirements record; `T-010` (Architecture ADR) unblocked; implementation (`T-011`) proceeds only after the ADR is fixed.
