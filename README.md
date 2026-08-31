# canyou

**canyou** is an **Agent-Ready Repository**: a baseline where the repository itself — not any agent's memory or any chat history — is the single source of truth for work state, evidence, and continuation. Any agent (Arena, Claude Code, Codex, Cursor, …) or human can open it and know exactly: *what happened, what remains, and what is the proof.*

> **Current status:** governance layer complete + **signed Product Definition** (`docs/PRODUCT.md`). First implementation phase scoped to a thin slice (Tool Registry + Policy Gate + one Connector); **no application code exists yet** — see `tasks/CURRENT.md`. Documentation here never counts as proof of implementation.

## How it works

1. [`AGENTS.md`](AGENTS.md) — the operating contract for **any** agent: neutral, no vendor-specific rules. It fixes the mandatory lifecycle
   `READ → UNDERSTAND → EXECUTE → VERIFY → DOCUMENT EVIDENCE → COMMIT → UPDATE STATE → HANDOFF`
   and the state vocabulary every claim must carry:

   | State | Meaning | Evidence |
   |---|---|---|
   | `DOCUMENTED` | Described in docs only | File path + heading |
   | `PREPARED` | Content exists, not at its operational location | Path to staged content |
   | `IMPLEMENTED` | Present at its operational location | Path(s) |
   | `VERIFIED` | Passed a deterministic check | Command + output |
   | `COMMITTED` | Fixed in Git history | Commit SHA |
   | `HANDOFF_READY` | Another agent can resume | Handoff record |

   Absence is recorded first-class as `NOT INSTALLED` / `NOT VERIFIED` — a negation never counts as its positive state.

2. **State lives in the repository:** `tasks/CURRENT.md` (now), `tasks/BACKLOG.md` (next), `docs/HANDOFF.md` (continuation records).

3. **Claims are verified, not trusted:** `bash scripts/verify/verify.sh` checks structure, content discipline, and hygiene — offline, deterministic, and (once activated per `T-008`) enforced by CI.

## Repository layout

```text
canyou/
├── AGENTS.md                    # Agent operating contract (agent-neutral)
├── README.md                    # This overview
├── CONTRIBUTING.md              # Contribution rules (humans + agents)
├── CHANGELOG.md                 # Human-readable history
├── docs/
│   ├── ARCHITECTURE.md          # What exists (and what does not)
│   ├── DEVELOPMENT.md           # Practical workflow manual
│   ├── OPERATIONS.md            # CI, releases, maintenance
│   ├── SECURITY.md              # Reporting, secrets, permissions
│   └── HANDOFF.md               # Continuation protocol + records
├── tasks/
│   ├── BACKLOG.md               # Queued work
│   └── CURRENT.md               # Current work state (read first)
├── scripts/verify/              # Deterministic verification suite
└── .github/                     # CI + issue/PR templates
```

## Quick start

```bash
git clone https://github.com/elazamey/canyou.git
cd canyou
bash scripts/verify/verify.sh   # must pass before any work
```

Then, if you are an agent: read [`AGENTS.md`](AGENTS.md) — it is binding. Then read [`tasks/CURRENT.md`](tasks/CURRENT.md).

## Documentation

| Doc | Purpose |
|---|---|
| [`AGENTS.md`](AGENTS.md) | Operating contract for all agents |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | What exists today (governance layer only) |
| [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md) | How to work on this repository |
| [`docs/OPERATIONS.md`](docs/OPERATIONS.md) | CI, verification suite, releases |
| [`docs/SECURITY.md`](docs/SECURITY.md) | Reporting vulnerabilities, secrets policy |
| [`docs/HANDOFF.md`](docs/HANDOFF.md) | Continuation protocol + handoff records |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How contributions are accepted |

## License

[MIT](LICENSE)
