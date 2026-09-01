"""R-2/R-4/R-5 — the gated chain: Gate before execution, no bypass, one record.

R-2 acceptance (verbatim): invoke an allowed tool (executed); invoke a tool
with a DENY policy (blocked, reason recorded); invoke with no matching
policy rule (DENY). R-4 acceptance: a bypass attempt fails by design.
R-5 acceptance: exactly one record per attempt.
"""

from __future__ import annotations

import unittest

from canyou import (
    DENIED,
    ERROR,
    EXECUTED,
    NOT_FOUND,
    Decision,
    PolicyGate,
    PolicyRule,
    Runtime,
    ToolContract,
    ToolRegistry,
    build_github_runtime,
)
from canyou.registry import RiskLevel

from helpers import FakeTransport, make_contract, make_response


def make_runtime(rules=()):
    registry = ToolRegistry()
    runtime = Runtime(registry=registry, policy=PolicyGate(rules))
    return runtime, registry


class RecordingExecutor:
    """Stub executor that records every call it receives."""

    def __init__(self, result="ok"):
        self.calls = []
        self.result = result

    def __call__(self, arguments):
        self.calls.append(dict(arguments))
        return self.result


class GateBeforeExecution(unittest.TestCase):
    def test_allowed_tool_executes(self):
        runtime, _ = make_runtime(
            [PolicyRule(tool_id="echo.tool", decision=Decision.ALLOW)]
        )
        executor = RecordingExecutor()
        runtime.register_contract(make_contract(name="echo.tool"))
        runtime.bind_executor("echo.tool", executor)
        result = runtime.execute("agent-1", "echo.tool", {"x": 1})
        self.assertEqual(result.status, EXECUTED)
        self.assertEqual(result.value, "ok")
        self.assertEqual(executor.calls, [{"x": 1}])

    def test_deny_policy_blocks_execution_and_records_reason(self):
        runtime, _ = make_runtime(
            [PolicyRule(tool_id="echo.tool", decision=Decision.DENY)]
        )
        executor = RecordingExecutor()
        runtime.register_contract(make_contract(name="echo.tool"))
        runtime.bind_executor("echo.tool", executor)
        result = runtime.execute("agent-1", "echo.tool", {})
        self.assertEqual(result.status, DENIED)
        self.assertEqual(result.policy_reason, "EXPLICIT_DENY")
        self.assertEqual(executor.calls, [])  # the executor is never reached

    def test_no_matching_rule_means_default_deny(self):
        runtime, _ = make_runtime()
        executor = RecordingExecutor()
        runtime.register_contract(make_contract(name="echo.tool"))
        runtime.bind_executor("echo.tool", executor)
        result = runtime.execute("agent-1", "echo.tool", {})
        self.assertEqual(result.status, DENIED)
        self.assertEqual(result.policy_reason, "DEFAULT_DENY")
        self.assertEqual(executor.calls, [])


class AttemptAccounting(unittest.TestCase):
    def test_exactly_one_record_per_attempt(self):
        runtime, _ = make_runtime(
            [PolicyRule(tool_id="echo.tool", decision=Decision.ALLOW)]
        )
        runtime.register_contract(make_contract(name="echo.tool"))
        runtime.bind_executor("echo.tool", RecordingExecutor())
        runtime.execute("a", "echo.tool", {})
        runtime.execute("a", "ghost.tool", {})
        runtime.execute("a", "echo.tool", {})
        self.assertEqual(len(runtime.evidence), 3)
        for record in runtime.evidence.records():
            self.assertTrue(record.execution_id)
            self.assertTrue(record.timestamp)
            self.assertIn(record.policy_decision, ("ALLOW", "DENY"))
            self.assertTrue(record.input_reference)
            self.assertTrue(record.output_reference)

    def test_unknown_tool_is_not_found_and_denied(self):
        runtime, _ = make_runtime()
        result = runtime.execute("a", "ghost.tool", {})
        self.assertEqual(result.status, NOT_FOUND)
        self.assertEqual(result.policy_reason, "TOOL_NOT_REGISTERED")
        self.assertEqual(len(runtime.evidence), 1)

    def test_executor_failure_fails_closed_but_records_exactly_once(self):
        runtime, _ = make_runtime(
            [PolicyRule(tool_id="boom.tool", decision=Decision.ALLOW)]
        )
        runtime.register_contract(make_contract(name="boom.tool"))

        def explode(arguments):
            raise ValueError("no")

        runtime.bind_executor("boom.tool", explode)
        result = runtime.execute("a", "boom.tool", {})
        self.assertEqual(result.status, ERROR)
        self.assertEqual(len(runtime.evidence), 1)

    def test_evidence_records_hashes_not_payloads(self):
        runtime, _ = make_runtime(
            [PolicyRule(tool_id="echo.tool", decision=Decision.ALLOW)]
        )
        runtime.register_contract(make_contract(name="echo.tool"))
        runtime.bind_executor("echo.tool", RecordingExecutor())
        secret = "agent-secret-value-77"
        runtime.execute("a", "echo.tool", {"token": secret})
        self.assertNotIn(secret, runtime.evidence.to_json_lines())


class NoBypass(unittest.TestCase):
    def test_public_surface_is_exactly_the_gated_api(self):
        runtime, _ = make_runtime()
        public = {name for name in dir(runtime) if not name.startswith("_")}
        self.assertEqual(
            public,
            {"register_contract", "bind_executor", "execute", "evidence"},
        )

    def test_no_connector_or_transport_wording_on_public_surface(self):
        runtime, _ = make_runtime()
        forbidden = ("connector", "transport", "bypass")
        public = [name for name in dir(runtime) if not name.startswith("_")]
        offenders = [
            word for word in forbidden if any(word in name.lower() for name in public)
        ]
        self.assertEqual(offenders, [])

    def test_registry_lookup_yields_contract_never_callable(self):
        _, registry = make_runtime()
        registry.register(make_contract(name="echo.tool"))
        looked_up = registry.lookup("echo.tool")
        self.assertIsInstance(looked_up, ToolContract)
        self.assertFalse(callable(looked_up))

    def test_binding_requires_a_registered_contract(self):
        runtime, _ = make_runtime()
        with self.assertRaises(ValueError):
            runtime.bind_executor("ghost.tool", lambda arguments: arguments)

    def test_double_binding_rejected(self):
        runtime, _ = make_runtime()
        runtime.register_contract(make_contract(name="echo.tool"))
        runtime.bind_executor("echo.tool", lambda arguments: arguments)
        with self.assertRaises(ValueError):
            runtime.bind_executor("echo.tool", lambda arguments: arguments)


class GitHubComposition(unittest.TestCase):
    def test_capability_without_policy_is_blocked_and_never_dials(self):
        transport = FakeTransport()
        runtime = build_github_runtime(transport=transport)
        result = runtime.execute(
            "agent-1",
            "github.read_file",
            {"owner": "o", "repo": "r", "path": "p"},
        )
        self.assertEqual(result.status, DENIED)
        self.assertEqual(result.policy_reason, "DEFAULT_DENY")
        self.assertEqual(transport.requests, [])  # existence is not permission

    def test_allowed_read_reaches_transport_exactly_once(self):
        transport = FakeTransport([make_response(200, '{"name":"f"}')])
        runtime = build_github_runtime(
            [PolicyRule(tool_id="github.read_file", decision=Decision.ALLOW)],
            transport=transport,
        )
        result = runtime.execute(
            "agent-1",
            "github.read_file",
            {"owner": "o", "repo": "r", "path": "p"},
        )
        self.assertEqual(result.status, EXECUTED)
        self.assertEqual(len(transport.requests), 1)
        self.assertEqual(len(runtime.evidence), 1)

    def test_destructive_class_never_runs_by_default(self):
        transport = FakeTransport()
        runtime = build_github_runtime(
            [PolicyRule(tool_id="github.merge_pull_request", decision=Decision.ALLOW)],
            transport=transport,
        )
        calls = []
        runtime.register_contract(
            make_contract(
                name="github.merge_pull_request",
                risk=RiskLevel.BLOCKED,
                permissions=("repo:write", "pr:merge"),
            )
        )
        runtime.bind_executor(
            "github.merge_pull_request", lambda arguments: calls.append(arguments)
        )
        result = runtime.execute("a", "github.merge_pull_request", {})
        self.assertEqual(result.status, DENIED)
        self.assertEqual(result.policy_reason, "DESTRUCTIVE_BLOCKED")
        self.assertEqual(calls, [])
        self.assertEqual(transport.requests, [])

    def test_composed_runtime_carries_the_four_architected_tools(self):
        runtime, registry = make_runtime()
        composed = build_github_runtime(transport=FakeTransport())
        self.assertEqual(
            composed._registry.tools(),  # noqa: SLF001 — test asserts composition
            (
                "github.commit_file",
                "github.create_branch",
                "github.create_pull_request",
                "github.read_file",
            ),
        )
        self.assertEqual(registry.tools(), ())


if __name__ == "__main__":
    unittest.main()
