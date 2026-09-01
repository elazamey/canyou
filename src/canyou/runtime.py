"""The gated execution chain — the only public path to execution (R-4).

Chain (directive section 7): Agent -> Tool Registry -> Policy Gate ->
bound executor -> Connector -> Evidence. The Runtime binds executors
privately; no public interface returns an executor, a connector, or a
transport, so the Gate cannot be bypassed through the public surface.
Every invocation attempt emits exactly one TraceRecord (R-5) — allowed,
denied, unknown tool, or error — always Gate-first, executor-only-on-ALLOW.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Iterable, Mapping, Optional

from .connectors.github import GitHubConnector, Transport, UrllibTransport
from .evidence import EvidenceLog, TraceRecord, reference_of
from .policy import Decision, PolicyDecision, PolicyGate, PolicyRule
from .registry import RiskLevel, ToolContract, ToolNotFound, ToolRegistry

EXECUTED = "EXECUTED"
DENIED = "DENIED"
NOT_FOUND = "NOT_FOUND"
ERROR = "ERROR"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_execution_id() -> str:
    return uuid.uuid4().hex


@dataclass(frozen=True)
class ExecutionResult:
    """Outcome of one invocation attempt; never raises for policy outcomes."""

    execution_id: str
    tool_id: str
    status: str
    policy_decision: str
    policy_reason: str
    value: Any = None
    error: Optional[str] = None


class Runtime:
    """Composes Registry + Policy Gate + privately bound executors + Evidence."""

    def __init__(
        self,
        registry: ToolRegistry,
        policy: PolicyGate,
        evidence: EvidenceLog | None = None,
        clock: Callable[[], str] = _utc_now,
        execution_id_factory: Callable[[], str] = _new_execution_id,
    ) -> None:
        self._registry = registry
        self._policy = policy
        self._evidence = evidence if evidence is not None else EvidenceLog()
        self._clock = clock
        self._execution_id_factory = execution_id_factory
        self._executors: Dict[str, Callable[[Mapping[str, Any]], Any]] = {}

    def register_contract(self, contract: ToolContract) -> None:
        """Register a declared contract (configuration, not execution)."""
        self._registry.register(contract)

    def bind_executor(
        self, tool_id: str, executor: Callable[[Mapping[str, Any]], Any]
    ) -> None:
        """Bind the implementation of an already-registered tool.

        The binding is stored privately and is never returned by any public
        interface, so callers cannot invoke it around the Gate (R-4).
        """
        if not self._registry.has(tool_id):
            raise ValueError(f"cannot bind executor: tool not registered: {tool_id}")
        if tool_id in self._executors:
            raise ValueError(f"executor already bound: {tool_id}")
        if not callable(executor):
            raise ValueError("executor must be callable")
        self._executors[tool_id] = executor

    def execute(
        self,
        agent_id: str,
        tool_id: str,
        arguments: Mapping[str, Any] | None = None,
    ) -> ExecutionResult:
        """Run one gated attempt: Gate first; the executor runs only on ALLOW."""
        execution_id = self._execution_id_factory()
        args = dict(arguments or {})
        input_reference = reference_of({"tool_id": tool_id, "arguments": args})
        try:
            contract = self._registry.lookup(tool_id)
        except ToolNotFound:
            contract = None
        decision: PolicyDecision = self._policy.decide(contract)

        status = DENIED
        value: Any = None
        error: Optional[str] = None
        if decision.decision is Decision.ALLOW:
            executor = self._executors.get(tool_id)
            if executor is None:
                status, error = ERROR, "RuntimeConfigurationError: no executor bound"
            else:
                try:
                    value = executor(args)
                    status = EXECUTED
                except Exception as exc:  # fail closed; the attempt is recorded
                    status, value, error = ERROR, None, type(exc).__name__
        elif contract is None:
            status = NOT_FOUND

        output_reference = reference_of(
            {"execution_id": execution_id, "outcome": status, "error": error}
        )
        self._evidence.append(
            TraceRecord(
                execution_id=execution_id,
                agent_id=agent_id,
                tool_id=tool_id,
                timestamp=self._clock(),
                policy_decision=decision.decision.value,
                policy_reason=decision.reason,
                input_reference=input_reference,
                output_reference=output_reference,
                artifact_reference=None,
            )
        )
        return ExecutionResult(
            execution_id=execution_id,
            tool_id=tool_id,
            status=status,
            policy_decision=decision.decision.value,
            policy_reason=decision.reason,
            value=value,
            error=error,
        )

    @property
    def evidence(self) -> EvidenceLog:
        """The run's append-only evidence log (R-5, directive section 8)."""
        return self._evidence


def build_github_runtime(
    policy_rules: Iterable[PolicyRule] = (),
    transport: Optional[Transport] = None,
) -> Runtime:
    """Production composition of the slice (directive section 7 chain).

    The GitHub connector and its transport are captured inside tool closures
    and are never exposed through the returned Runtime (R-4). Pass
    ``transport`` in tests to run fully offline (R-6); by default a stdlib
    ``urllib`` transport reads the token from the environment at call time
    (constraints area 6 — secrets never reach callers or evidence).
    """
    connector = GitHubConnector(
        transport if transport is not None else UrllibTransport()
    )
    registry = ToolRegistry()
    runtime = Runtime(registry=registry, policy=PolicyGate(policy_rules))

    def add_tool(contract: ToolContract, operation: str) -> None:
        runtime.register_contract(contract)
        runtime.bind_executor(
            contract.name,
            lambda arguments, bound_operation=operation: connector.call(
                bound_operation, arguments
            ),
        )

    add_tool(
        ToolContract(
            name="github.read_file",
            description="Read a file from a GitHub repository",
            permissions=("repo:read",),
            risk=RiskLevel.LOW,
            audit_note="records read access to repository contents",
        ),
        "read_file",
    )
    add_tool(
        ToolContract(
            name="github.create_branch",
            description="Create a new branch from an existing base branch",
            permissions=("repo:write",),
            risk=RiskLevel.MEDIUM,
            audit_note="records branch creation in a repository",
        ),
        "create_branch",
    )
    add_tool(
        ToolContract(
            name="github.commit_file",
            description="Commit one file to a branch",
            permissions=("repo:write",),
            risk=RiskLevel.MEDIUM,
            audit_note="records file commits to a branch",
        ),
        "commit_file",
    )
    add_tool(
        ToolContract(
            name="github.create_pull_request",
            description="Open a pull request",
            permissions=("repo:write", "pr:create"),
            risk=RiskLevel.MEDIUM,
            audit_note="records pull request creation",
        ),
        "create_pull_request",
    )
    return runtime
