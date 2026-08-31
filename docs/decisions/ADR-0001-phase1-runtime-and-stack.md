# ADR-0001: Phase-1 runtime language and stack — Python 3.11+, stdlib-only

- **Status:** ACCEPTED
- **Date:** 2026-08-31
- **Deciders:** repository owner — OWNER DIRECTIVE §4-C (evaluation delegated to the agent under mandatory criteria: actual requirements, cost, free operability, security, scalability); executed by Arena Agent
- **Sources:** `docs/REQUIREMENTS.md` (SIGNED: R-1..R-7 + directive addendum §6/§7/§8/§9), `docs/CONSTRAINTS.md` (nine rules, six areas, directive decision rows), `docs/PRODUCT.md` (signed definition)

## Context

- The signed requirements fix the Phase-1 slice: Tool Registry, default-DENY Policy Gate, exactly one connector (**GitHub** — owner selection, directive §7), no path around the Gate, minimal per-operation trace records, free-to-build/run/verify **offline**, and strict non-goals (R-7).
- Directive §4-C criteria: evaluate against actual requirements, not preference; priorities are cost, free operability, security, scalability; “TypeScript first **if the repository is already TypeScript**” — the repository contains **zero application code**, so that rule does not apply.
- Constraints: FREE TO BUILD/RUN/DEPLOY, NO CREDIT CARD; provider abstraction mandatory (future Gemini / Hugging Face / local providers — never the heart of the system); no model training; secrets never reach the agent/model.
- Operational constraint: `.github/workflows/ci.yml` cannot be edited by the automation token (documented `workflows`-permission rejections) — so the stack should let CI gate the slice **without workflow changes**.

## Decision

1. **Language: Python 3.11+** for the Phase-1 runtime (`src/canyou/` package).
2. **Zero third-party runtime dependencies in Phase 1.** GitHub REST access via stdlib `urllib.request`; tests via stdlib `unittest`. Dev tooling adds nothing paid and nothing card-gated.
3. **Layout:** `src/canyou/registry.py` (Tool Registry + ToolContract), `src/canyou/policy.py` (Policy Gate, default DENY), `src/canyou/connectors/` (Connector interface + `github.py` adapter), `src/canyou/evidence.py` (TraceRecord), `src/canyou/runtime.py` (the gated execution chain). Tests under `tests/`.
4. **CI without workflow edits:** a new check `scripts/verify/verify_slice.sh` runs `python3 -m unittest discover -s tests` inside the existing `verify.sh` entry point — every push stays gated on slice tests; the workflow file is untouched (Python 3.11 is preinstalled, free, on ubuntu-latest).
5. **Security shape (directive §6 / R-1, R-2):** every ToolContract declares identity, permissions, risk level (LOW / MEDIUM / HIGH / BLOCKED), approval requirement, audit fields. Default policy = DENY; destructive operations (merge/delete-class) are BLOCKED unless explicitly enabled by a policy entry — never granted by default.
6. **Traceability shape (directive §8 / R-5):** `evidence.TraceRecord` carries `execution_id`, `agent_id`, `tool_id`, `timestamp`, `policy_decision`, input/output evidence references, optional artifact reference; append-only within a run (JSON-lines). This is the minimal record — deliberately not an Execution Ledger system.

## Alternatives considered

- **TypeScript / Node.js** — strong GitHub ecosystem (octokit), unifies a future UI and runtime; **rejected for Phase 1**: the repository is not TypeScript (directive rule inapplicable), and the npm supply-chain surface conflicts with the zero-dependency free-first posture; requires a Node toolchain on every verifying machine.
- **Go** — excellent single-binary deployment and concurrency; **deferred, not rejected**: viable later, but the eventual AI-provider layer (Hugging Face / local models) has a materially closer ecosystem in Python, and area-1/3 deferral must not be precluded.
- **Rust** — maximal safety and performance; **rejected for Phase 1**: iteration cost for a governance MVP outweighs the benefit at this slice’s size.

## Consequences

- **(+) R-6 trivially satisfied:** no dependencies → offline build/test/verify everywhere; CI unchanged and free.
- **(+) Provider abstraction preserved (§9):** providers remain future adapters behind interfaces; nothing here hard-codes a vendor; model integration stays a Phase-1 non-goal (R-7).
- **(+) Secrets posture (§6):** credentials live only inside the Connector Runtime (read from environment at call time), never in tool contracts, never in agent-facing surfaces.
- **(−)** stdlib `urllib` is lower-level than octokit/requests — acceptable: the Phase-1 GitHub surface is small (read file / create branch / commit / create PR) and isolated behind the connector adapter.
- **(−)** Future provider adapters may need third-party libraries — permitted later **only via a new ADR**, never silently.

## Compliance check (directive §12 stop-rules)

No conflict with any signed requirement found: R-1..R-7 and the directive addendum were checked item-by-item; this ADR implements them and opens none of the §5 exclusions. Q-2’s deferred discussion (CONSTRAINTS decision row) is concluded here, per directive §4-C authorization.
