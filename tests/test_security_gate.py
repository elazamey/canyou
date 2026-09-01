"""T-012 — Security Gate harness over the ten signed review axes.

Axes (tasks/BACKLOG.md T-012, docs/ROADMAP.md §3 — verbatim intent):
authentication, authorization, least privilege, secrets handling, connector
isolation, policy-bypass resistance, evidence integrity, network failure,
timeout handling, error handling. Each axis below is a class whose name is
the axis token; ``scripts/verify/verify_security.sh`` (check 5) greps these
tokens so a silently dropped axis fails the gate instead of passing unseen.

Findings closed by this harness (re-implemented from the documented
specification after the original T-012 commits were lost un-pushed; see
tasks/CURRENT.md → Verified Facts):

- SEC-1 authorization: ``requires_approval`` was declared-but-unenforced on
  ToolContract (directive §6) — an approval-gated tool ran on a plain ALLOW.
  Phase 1 has no approval mechanism (R-7 non-goal), so the gate now fails
  closed with APPROVAL_REQUIRED.
- SEC-2 least privilege: no bound on permission *names*. The Phase-1
  composition now carries PHASE1_PERMISSIONS; any grant or declaration
  outside the ceiling is DENYed with UNKNOWN_PERMISSION (e.g. issue-writing
  would need ``issues:write`` — rejected by design until a slice adds the
  operation, the declared contract, the ceiling entry, and the tests).
- SEC-3 connector isolation: payload values interpolated into provider URL
  paths are now percent-encoded per segment.
- SEC-4 network/timeout/secrets: redirects are never followed (the bearer
  token cannot be re-sent off origin); timeout and connection-reset errors
  are wrapped like every other transport failure; blank tokens are missing.
- SEC-5 error handling: malformed/non-JSON 2xx bodies fail closed as
  GitHubConnectorError; executor error *messages* never surface (type only).
- SEC-6 evidence integrity: the Runtime hands out a read-only EvidenceView;
  forging an appended record through the public surface is impossible.

Everything here is offline (R-6): fake transports, fake openers, and the
stdlib only. No test dials a network.
"""

from __future__ import annotations

import dataclasses
import io
import os
import unittest
import urllib.error
from datetime import datetime, timezone
from typing import Any, List, Optional

from canyou import (
    DENIED,
    ERROR,
    EXECUTED,
    NOT_FOUND,
    Decision,
    PolicyGate,
    PolicyRule,
    RiskLevel,
    Runtime,
    ToolContract,
    ToolRegistry,
    build_github_runtime,
)
from canyou.connectors import Connector, GitHubConnector
from canyou.connectors.github import (
    GitHubConnectorError,
    GitHubRequest,
    GitHubTokenMissing,
    UrllibTransport,
    _NoRedirectHandler,
)
from canyou.evidence import TraceRecord, reference_of
from canyou.policy import PHASE1_PERMISSIONS
from canyou.runtime import EvidenceView

from helpers import FakeTransport, make_contract, make_response


# --------------------------------------------------------------------------
# Offline doubles for the REAL transport seam (UrllibTransport._opener).
# --------------------------------------------------------------------------


class FakeHTTPResponse:
    """Minimal stand-in for the object urllib returns on success."""

    def __init__(self, body: bytes = b"{}", status: int = 200) -> None:
        self._body = body
        self.status = status

    def read(self) -> bytes:
        return self._body

    def __enter__(self) -> "FakeHTTPResponse":
        return self

    def __exit__(self, *exc: Any) -> bool:
        return False


class RecordingOpener:
    """Opener stand-in: records every open() call, replays one outcome."""

    def __init__(self, outcome: Any) -> None:
        self.outcome = outcome  # FakeHTTPResponse, or an Exception to raise
        self.calls: List[Any] = []

    def open(self, http_request: Any, timeout: Optional[int] = None) -> Any:
        self.calls.append({"request": http_request, "timeout": timeout})
        if isinstance(self.outcome, Exception):
            raise self.outcome
        return self.outcome


def make_transport(outcome: Any, **kwargs: Any) -> Any:
    """Real UrllibTransport wired to a recording opener (zero network)."""
    transport = UrllibTransport(**kwargs)
    recording = RecordingOpener(outcome)
    transport._opener = recording  # noqa: SLF001 — test asserts transport behavior
    return transport, recording


def make_record(**overrides: Any) -> TraceRecord:
    fields = dict(
        execution_id="exec-forge",
        agent_id="agent-x",
        tool_id="github.read_file",
        timestamp="2026-09-01T00:00:00+00:00",
        policy_decision="ALLOW",
        policy_reason="EXPLICIT_ALLOW",
        input_reference="in-ref",
        output_reference="out-ref",
    )
    fields.update(overrides)
    return TraceRecord(**fields)


class RecordingExecutor:
    def __init__(self, result: Any = "ok") -> None:
        self.calls: List[Any] = []
        self.result = result

    def __call__(self, arguments: Any) -> Any:
        self.calls.append(dict(arguments))
        return self.result


# --------------------------------------------------------------------------
# Axis 1 — authentication
# --------------------------------------------------------------------------


class Authentication(unittest.TestCase):
    """T-012 axis: authentication — token presence, freshness, placement."""

    def test_missing_token_refuses_before_any_round_trip(self):
        transport, recording = make_transport(FakeHTTPResponse())
        with _cleared_token_env():
            with self.assertRaises(GitHubTokenMissing) as context:
                transport.request(GitHubRequest(method="GET", path="/x"))
        self.assertIsInstance(context.exception, GitHubConnectorError)
        self.assertEqual(context.exception.status, 0)  # no HTTP round trip
        self.assertEqual(recording.calls, [])

    def test_blank_or_whitespace_token_is_treated_as_missing(self):
        transport, recording = make_transport(FakeHTTPResponse())
        with _patched_token("   \t  "):
            with self.assertRaises(GitHubTokenMissing):
                transport.request(GitHubRequest(method="GET", path="/x"))
        self.assertEqual(recording.calls, [])

    def test_token_is_read_from_the_environment_at_call_time(self):
        transport, recording = make_transport(FakeHTTPResponse())
        with _patched_token("tok-first"):
            transport.request(GitHubRequest(method="GET", path="/a"))
        with _patched_token("tok-second"):
            transport.request(GitHubRequest(method="GET", path="/b"))
        first = recording.calls[0]["request"].get_header("Authorization")
        second = recording.calls[1]["request"].get_header("Authorization")
        self.assertEqual(first, "Bearer tok-first")
        self.assertEqual(second, "Bearer tok-second")  # re-read, never stored

    def test_bearer_header_is_attached_exactly_once_with_api_version(self):
        transport, recording = make_transport(FakeHTTPResponse())
        with _patched_token("tok-secret-123"):
            transport.request(GitHubRequest(method="GET", path="/x"))
        sent = recording.calls[0]["request"]
        auth_values = [
            value
            for name, value in sent.header_items()
            if name.lower() == "authorization"
        ]
        self.assertEqual(auth_values, ["Bearer tok-secret-123"])
        headers = {name.lower(): value for name, value in sent.header_items()}
        self.assertEqual(headers["x-github-api-version"], "2022-11-28")
        self.assertTrue(headers["user-agent"])


# --------------------------------------------------------------------------
# Axis 2 — authorization (incl. SEC-1 approval requirements)
# --------------------------------------------------------------------------


class Authorization(unittest.TestCase):
    """T-012 axis: authorization — decisions are explicit, approvals real."""

    def test_requires_approval_is_enforced_not_silently_ignored(self):
        gate = PolicyGate([PolicyRule(tool_id="appr.tool", decision=Decision.ALLOW)])
        contract = make_contract(name="appr.tool")
        contract = dataclasses.replace(contract, requires_approval=True)
        outcome = gate.decide(contract)
        self.assertIs(outcome.decision, Decision.DENY)
        self.assertEqual(outcome.reason, "APPROVAL_REQUIRED")

    def test_approval_gated_tool_runs_no_executor(self):
        runtime = Runtime(registry=ToolRegistry(), policy=PolicyGate(
            [PolicyRule(tool_id="appr.tool", decision=Decision.ALLOW)]
        ))
        runtime.register_contract(
            dataclasses.replace(make_contract(name="appr.tool"), requires_approval=True)
        )
        executor = RecordingExecutor()
        runtime.bind_executor("appr.tool", executor)
        result = runtime.execute("agent-1", "appr.tool", {})
        self.assertEqual(result.status, DENIED)
        self.assertEqual(result.policy_reason, "APPROVAL_REQUIRED")
        self.assertEqual(executor.calls, [])

    def test_approval_denial_is_recorded_exactly_once(self):
        runtime = Runtime(registry=ToolRegistry(), policy=PolicyGate(
            [PolicyRule(tool_id="appr.tool", decision=Decision.ALLOW)]
        ))
        runtime.register_contract(
            dataclasses.replace(make_contract(name="appr.tool"), requires_approval=True)
        )
        runtime.bind_executor("appr.tool", RecordingExecutor())
        runtime.execute("agent-1", "appr.tool", {})
        self.assertEqual(len(runtime.evidence), 1)
        (record,) = runtime.evidence.records()
        self.assertEqual(record.policy_decision, "DENY")
        self.assertEqual(record.policy_reason, "APPROVAL_REQUIRED")

    def test_capability_without_policy_remains_blocked(self):
        transport = FakeTransport()
        runtime = build_github_runtime(transport=transport)
        result = runtime.execute(
            "agent-1",
            "github.create_pull_request",
            {"owner": "o", "repo": "r", "head": "h", "base": "b", "title": "t"},
        )
        self.assertEqual(result.status, DENIED)
        self.assertEqual(result.policy_reason, "DEFAULT_DENY")
        self.assertEqual(transport.requests, [])  # existence is not permission

    def test_allowed_within_the_ceiling_executes(self):
        transport = FakeTransport([make_response(200, '{"name":"f"}')])
        runtime = build_github_runtime(
            [PolicyRule(tool_id="github.read_file", decision=Decision.ALLOW)],
            transport=transport,
        )
        result = runtime.execute(
            "agent-1", "github.read_file", {"owner": "o", "repo": "r", "path": "p"}
        )
        self.assertEqual(result.status, EXECUTED)
        self.assertEqual(len(transport.requests), 1)

    def test_blocked_class_is_denied_before_the_ceiling_is_consulted(self):
        # Destructive containment dominates capability naming: the reason for
        # this veto must stay DESTRUCTIVE_BLOCKED even when the destructive
        # contract also declares a permission outside the ceiling.
        transport = FakeTransport()
        runtime = build_github_runtime(
            [PolicyRule(tool_id="github.merge_pull_request", decision=Decision.ALLOW)],
            transport=transport,
        )
        runtime.register_contract(
            make_contract(
                name="github.merge_pull_request",
                risk=RiskLevel.BLOCKED,
                permissions=("repo:write", "pr:merge"),
            )
        )
        runtime.bind_executor("github.merge_pull_request", RecordingExecutor())
        result = runtime.execute("agent-1", "github.merge_pull_request", {})
        self.assertEqual(result.status, DENIED)
        self.assertEqual(result.policy_reason, "DESTRUCTIVE_BLOCKED")
        self.assertEqual(transport.requests, [])


# --------------------------------------------------------------------------
# Axis 3 — least privilege (SEC-2 permission ceiling)
# --------------------------------------------------------------------------


class LeastPrivilege(unittest.TestCase):
    """T-012 axis: least privilege — authority bounded by a closed name set."""

    def test_phase1_ceiling_is_the_exact_signed_set(self):
        self.assertEqual(
            set(PHASE1_PERMISSIONS), {"repo:read", "repo:write", "pr:create"}
        )

    def test_all_shipped_contracts_stay_inside_the_ceiling(self):
        runtime = build_github_runtime(transport=FakeTransport())
        registry = runtime._registry  # noqa: SLF001 — test asserts composition
        self.assertEqual(len(registry), 4)
        for name in registry.tools():
            declared = set(registry.lookup(name).permissions)
            self.assertLessEqual(
                declared,
                PHASE1_PERMISSIONS,
                f"{name} declares {sorted(declared - PHASE1_PERMISSIONS)}",
            )

    def test_out_of_ceiling_operation_is_rejected_by_design(self):
        # The "github.issue.create" shape: not in the connector, and the
        # permission it would need ("issues:write") is outside the ceiling.
        # Expected friction, not a malfunction: zero transport, one trace.
        transport = FakeTransport()
        runtime = build_github_runtime(
            [PolicyRule(tool_id="github.issue.create", decision=Decision.ALLOW)],
            transport=transport,
        )
        runtime.register_contract(
            make_contract(name="github.issue.create", permissions=("issues:write",))
        )
        executor = RecordingExecutor()
        runtime.bind_executor("github.issue.create", executor)
        result = runtime.execute("agent-1", "github.issue.create", {"title": "t"})
        self.assertEqual(result.status, DENIED)
        self.assertEqual(result.policy_reason, "UNKNOWN_PERMISSION")
        self.assertEqual(executor.calls, [])  # executor never reached
        self.assertEqual(transport.requests, [])  # zero provider round trips
        self.assertEqual(len(runtime.evidence), 1)  # exactly one trace record
        (record,) = runtime.evidence.records()
        self.assertEqual(record.policy_reason, "UNKNOWN_PERMISSION")

    def test_denial_detail_lists_the_offending_names_sorted(self):
        gate = PolicyGate(
            [PolicyRule(tool_id="x.tool", decision=Decision.ALLOW)],
            permission_ceiling=PHASE1_PERMISSIONS,
        )
        contract = make_contract(
            name="x.tool", permissions=("repo:read", "zzz:bad", "aaa:bad")
        )
        outcome = gate.decide(contract)
        self.assertIs(outcome.decision, Decision.DENY)
        self.assertEqual(outcome.reason, "UNKNOWN_PERMISSION")
        self.assertIn("aaa:bad, zzz:bad", outcome.detail)
        self.assertNotIn("repo:read", outcome.detail)  # in-ceiling, not named

    def test_one_bad_permission_fails_the_whole_declaration(self):
        gate = PolicyGate(
            [PolicyRule(tool_id="mix.tool", decision=Decision.ALLOW)],
            permission_ceiling=PHASE1_PERMISSIONS,
        )
        outcome = gate.decide(
            make_contract(name="mix.tool", permissions=("repo:read", "org:admin"))
        )
        self.assertIs(outcome.decision, Decision.DENY)
        self.assertEqual(outcome.reason, "UNKNOWN_PERMISSION")

    def test_ceiling_is_a_composition_posture_not_the_default_gate(self):
        # The plain gate stays agnostic (existing tools/tests keep their own
        # permission names); only compositions that opt in are bounded.
        gate = PolicyGate([PolicyRule(tool_id="any.tool", decision=Decision.ALLOW)])
        outcome = gate.decide(make_contract(name="any.tool", permissions=("t:use",)))
        self.assertIs(outcome.decision, Decision.ALLOW)

    def test_explicit_deny_still_wins_over_a_ceiling_violation(self):
        gate = PolicyGate(
            [
                PolicyRule(tool_id="x.tool", decision=Decision.ALLOW),
                PolicyRule(tool_id="x.tool", decision=Decision.DENY),
            ],
            permission_ceiling=PHASE1_PERMISSIONS,
        )
        outcome = gate.decide(make_contract(name="x.tool", permissions=("bad:x",)))
        self.assertIs(outcome.decision, Decision.DENY)
        self.assertEqual(outcome.reason, "EXPLICIT_DENY")

    def test_default_deny_still_precedes_ceiling_evaluation(self):
        gate = PolicyGate([], permission_ceiling=PHASE1_PERMISSIONS)
        outcome = gate.decide(make_contract(name="x.tool", permissions=("bad:x",)))
        self.assertIs(outcome.decision, Decision.DENY)
        self.assertEqual(outcome.reason, "DEFAULT_DENY")


# --------------------------------------------------------------------------
# Axis 4 — secrets handling
# --------------------------------------------------------------------------


class SecretsHandling(unittest.TestCase):
    """T-012 axis: secrets — no storage, no echo, no redirect exfiltration."""

    def test_transport_instance_state_never_contains_the_token(self):
        transport, _ = make_transport(FakeHTTPResponse())
        with _patched_token("tok-secret-123"):
            transport.request(GitHubRequest(method="GET", path="/x"))
        self.assertNotIn("tok-secret-123", repr(vars(transport)))

    def test_request_objects_have_no_credential_field_by_construction(self):
        field_names = {field.name for field in dataclasses.fields(GitHubRequest)}
        self.assertEqual(field_names, {"method", "path", "query", "body"})
        self.assertNotIn("token", {name.lower() for name in field_names})

    def test_provider_error_detail_is_capped(self):
        huge_body = b"x" * 4000
        outcome = urllib.error.HTTPError(
            "https://api.github.com/x", 500, "ISE", None, io.BytesIO(huge_body)
        )
        transport, _ = make_transport(outcome)
        with _patched_token("tok-secret-123"):
            with self.assertRaises(GitHubConnectorError) as context:
                transport.request(GitHubRequest(method="GET", path="/x"))
        self.assertEqual(context.exception.status, 500)
        self.assertLessEqual(len(context.exception.detail), 200)

    def test_denied_attempt_with_secret_argument_records_hashes_only(self):
        transport = FakeTransport()
        runtime = build_github_runtime(transport=transport)
        secret = "ghp_denied-secret-99"
        result = runtime.execute(
            "agent-1",
            "github.read_file",
            {"owner": "o", "repo": "r", "path": "p", "token": secret},
        )
        self.assertEqual(result.status, DENIED)
        self.assertNotIn(secret, runtime.evidence.to_json_lines())
        self.assertIn(
            reference_of(
                {
                    "tool_id": "github.read_file",
                    "arguments": {"owner": "o", "repo": "r", "path": "p", "token": secret},
                }
            ),
            runtime.evidence.to_json_lines(),
        )

    def test_failed_attempt_with_secret_argument_leaks_nothing(self):
        runtime, _registry = _allowing_runtime_with_executor(
            "boom.tool", RuntimeError("failure mentioning secret-value-77")
        )
        result = runtime.execute("a", "boom.tool", {"token": "secret-value-77"})
        self.assertEqual(result.status, ERROR)
        self.assertEqual(result.error, "RuntimeError")  # type name only
        self.assertNotIn("secret-value-77", repr(result.error))
        self.assertNotIn("secret-value-77", runtime.evidence.to_json_lines())

    def test_redirects_are_refused_at_the_handler_level(self):
        handler = _NoRedirectHandler()
        decision = handler.redirect_request(
            None, None, 302, "Found", {}, "https://attacker.example/collect"
        )
        self.assertIsNone(decision)  # refuse: never rebuild the request

    def test_the_transport_opener_carrier_refuses_redirects(self):
        # The REAL opener (not the recording double) must have the
        # no-redirect handler installed — this is where following (or not
        # following) a 3xx is actually decided.
        opener = UrllibTransport()._opener  # noqa: SLF001 — asserts composition
        self.assertTrue(
            any(isinstance(inst, _NoRedirectHandler) for inst in opener.handlers),
            "opener must install the no-redirect handler",
        )

    def test_a_3xx_response_is_treated_as_an_error_not_an_instruction(self):
        connector = GitHubConnector(
            FakeTransport([make_response(302, '{"url":"https://elsewhere/x"}')])
        )
        with self.assertRaises(GitHubConnectorError) as context:
            connector.call("read_file", {"owner": "o", "repo": "r", "path": "p"})
        self.assertEqual(context.exception.status, 302)


# --------------------------------------------------------------------------
# Axis 5 — connector isolation (SEC-3 route injection)
# --------------------------------------------------------------------------


class ConnectorIsolation(unittest.TestCase):
    """T-012 axis: connector isolation — payloads cannot rewrite routes."""

    def test_owner_segment_is_percent_encoded(self):
        transport = FakeTransport([make_response(200, "{}")])
        GitHubConnector(transport).call(
            "read_file", {"owner": "o/evil", "repo": "r", "path": "p"}
        )
        self.assertEqual(transport.requests[0].path, "/repos/o%2Fevil/r/contents/p")

    def test_repo_segment_cannot_carry_query_or_fragment(self):
        transport = FakeTransport([make_response(200, "{}")])
        GitHubConnector(transport).call(
            "read_file", {"owner": "o", "repo": "r?x=1#frag", "path": "p"}
        )
        self.assertEqual(
            transport.requests[0].path, "/repos/o/r%3Fx%3D1%23frag/contents/p"
        )

    def test_base_ref_in_create_branch_is_segment_encoded(self):
        transport = FakeTransport(
            [make_response(200, '{"object":{"sha":"s"}}'), make_response(201, '{"ref":"refs/heads/n"}')]
        )
        GitHubConnector(transport).call(
            "create_branch",
            {"owner": "o", "repo": "r", "base": "main/heads/x", "branch": "n"},
        )
        self.assertEqual(
            transport.requests[0].path, "/repos/o/r/git/ref/heads/main%2Fheads%2Fx"
        )

    def test_branch_name_lives_in_the_body_not_the_path(self):
        transport = FakeTransport(
            [make_response(200, '{"object":{"sha":"s"}}'), make_response(201, '{"ref":"refs/heads/f/x"}')]
        )
        result = GitHubConnector(transport).call(
            "create_branch",
            {"owner": "o", "repo": "r", "base": "main", "branch": "f/x"},
        )
        self.assertEqual(transport.requests[1].path, "/repos/o/r/git/refs")
        self.assertEqual(result["ref"], "refs/heads/f/x")  # provider validates

    def test_file_path_keeps_structure_slashes_but_encodes_spaces(self):
        transport = FakeTransport([make_response(200, "{}")])
        GitHubConnector(transport).call(
            "read_file", {"owner": "o", "repo": "r", "path": "docs/a b.md"}
        )
        self.assertEqual(
            transport.requests[0].path, "/repos/o/r/contents/docs/a%20b.md"
        )

    def test_adversarial_owner_cannot_reach_the_route_root(self):
        transport = FakeTransport([make_response(200, "{}")])
        GitHubConnector(transport).call(
            "read_file", {"owner": "../../admin", "repo": "r", "path": "p"}
        )
        sent = transport.requests[0].path
        # Every "/" inside the payload is encoded into the segment, so the
        # router still sees exactly five structural slashes — the value can
        # never escape its segment, whatever it spells.
        self.assertEqual(sent, "/repos/..%2F..%2Fadmin/r/contents/p")
        self.assertEqual(sent.count("/"), 5)

    def test_operations_surface_is_exactly_the_four_architected(self):
        self.assertEqual(
            GitHubConnector.OPERATIONS,
            frozenset(
                {"read_file", "create_branch", "commit_file", "create_pull_request"}
            ),
        )
        transport = FakeTransport()
        with self.assertRaises(GitHubConnectorError):
            GitHubConnector(transport).call("issue.create", {})
        self.assertEqual(transport.requests, [])  # refused before any dial


# --------------------------------------------------------------------------
# Axis 6 — policy-bypass resistance (incl. SEC-6 surface shape)
# --------------------------------------------------------------------------


class PolicyBypassResistance(unittest.TestCase):
    """T-012 axis: no path around the Gate, and the evidence sink is sealed."""

    def test_public_evidence_surface_is_the_read_only_view(self):
        runtime = build_github_runtime(transport=FakeTransport())
        self.assertIsInstance(runtime.evidence, EvidenceView)
        public = {
            name for name in dir(runtime.evidence) if not name.startswith("_")
        }
        self.assertEqual(public, {"records", "to_json_lines"})

    def test_no_public_runtime_attribute_yields_executor_connector_or_transport(self):
        runtime = build_github_runtime(transport=FakeTransport())
        for name in dir(runtime):
            if name.startswith("_"):
                continue
            value = getattr(runtime, name)
            self.assertNotIsInstance(value, GitHubConnector)
            self.assertNotIsInstance(value, Connector)

    def test_unknown_tool_never_dials_and_records_exactly_once(self):
        transport = FakeTransport()
        runtime = build_github_runtime(transport=transport)
        result = runtime.execute("agent-1", "ghost.tool", {"x": 1})
        self.assertEqual(result.status, NOT_FOUND)
        self.assertEqual(transport.requests, [])
        self.assertEqual(len(runtime.evidence), 1)

    def test_forging_a_record_through_the_public_surface_is_impossible(self):
        runtime = build_github_runtime(transport=FakeTransport())
        runtime.execute("agent-1", "ghost.tool", {})
        before = len(runtime.evidence)
        with self.assertRaises(AttributeError):
            runtime.evidence.append(make_record(execution_id="forged-1"))
        self.assertEqual(len(runtime.evidence), before)
        self.assertNotIn("forged-1", runtime.evidence.to_json_lines())

    def test_policy_facts_cannot_be_mutated_after_registration(self):
        contract = make_contract(name="frozen.tool")
        with self.assertRaises(dataclasses.FrozenInstanceError):
            contract.permissions = ("org:admin",)  # type: ignore[misc]
        rule = PolicyRule(tool_id="frozen.tool", decision=Decision.ALLOW)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            rule.decision = Decision.DENY  # type: ignore[misc]

    def test_duplicate_tool_names_are_rejected_as_shadowing(self):
        from canyou.registry import DuplicateToolError

        runtime = build_github_runtime(transport=FakeTransport())
        with self.assertRaises(DuplicateToolError):
            runtime.register_contract(
                make_contract(name="github.read_file", permissions=("repo:read",))
            )


# --------------------------------------------------------------------------
# Axis 7 — evidence integrity (SEC-6)
# --------------------------------------------------------------------------


class EvidenceIntegrity(unittest.TestCase):
    """T-012 axis: evidence — append-only, hash-bound, schema-fixed."""

    def test_record_schema_is_exactly_the_signed_field_set(self):
        names = {field.name for field in dataclasses.fields(TraceRecord)}
        self.assertEqual(
            names,
            {
                "execution_id",
                "agent_id",
                "tool_id",
                "timestamp",
                "policy_decision",
                "policy_reason",
                "input_reference",
                "output_reference",
                "artifact_reference",
            },
        )

    def test_records_snapshot_from_the_view_is_immutable(self):
        runtime = build_github_runtime(transport=FakeTransport())
        runtime.execute("agent-1", "ghost.tool", {})
        snapshot = runtime.evidence.records()
        with self.assertRaises(AttributeError):
            snapshot.append(make_record())  # type: ignore[attr-defined]
        self.assertEqual(len(runtime.evidence), 1)

    def test_every_attempt_binds_a_unique_execution_id(self):
        runtime = build_github_runtime(transport=FakeTransport())
        for _ in range(3):
            runtime.execute("agent-1", "ghost.tool", {})
        ids = [record.execution_id for record in runtime.evidence.records()]
        self.assertEqual(len(set(ids)), 3)
        self.assertTrue(all(ids))

    def test_timestamps_are_utc_isoformat(self):
        runtime = build_github_runtime(transport=FakeTransport())
        runtime.execute("agent-1", "ghost.tool", {})
        (record,) = runtime.evidence.records()
        parsed = datetime.fromisoformat(record.timestamp)
        self.assertIsNotNone(parsed.tzinfo)
        self.assertEqual(parsed.utcoffset(), timezone.utc.utcoffset(None))

    def test_output_reference_binds_the_outcome_of_the_attempt(self):
        denied = build_github_runtime(transport=FakeTransport())
        denied.execute("agent-1", "github.read_file", {"owner": "o", "repo": "r", "path": "p"})
        allowed = build_github_runtime(
            [PolicyRule(tool_id="github.read_file", decision=Decision.ALLOW)],
            transport=FakeTransport([make_response(200, '{"name":"f"}')]),
        )
        allowed.execute("agent-1", "github.read_file", {"owner": "o", "repo": "r", "path": "p"})
        (denied_record,) = denied.evidence.records()
        (allowed_record,) = allowed.evidence.records()
        self.assertEqual(denied_record.input_reference, allowed_record.input_reference)
        self.assertNotEqual(
            denied_record.output_reference, allowed_record.output_reference
        )  # the recorded outcome is content-bound, not boilerplate

    def test_json_lines_are_parseable_and_carry_reason_vocabulary(self):
        transport = FakeTransport()
        runtime = build_github_runtime(transport=transport)
        runtime.execute("agent-1", "ghost.tool", {})
        runtime.execute("agent-1", "github.read_file", {"owner": "o", "repo": "r", "path": "p"})
        import json

        lines = runtime.evidence.to_json_lines().splitlines()
        self.assertEqual(len(lines), 2)
        reasons = {json.loads(line)["policy_reason"] for line in lines}
        self.assertEqual(reasons, {"TOOL_NOT_REGISTERED", "DEFAULT_DENY"})


# --------------------------------------------------------------------------
# Axis 8 — network failure (SEC-4)
# --------------------------------------------------------------------------


class NetworkFailure(unittest.TestCase):
    """T-012 axis: network failure — one wrapped error shape, fail closed."""

    def test_url_error_is_wrapped_with_status_zero(self):
        outcome = urllib.error.URLError("nodename nor servname provided")
        transport, _ = make_transport(outcome)
        with _patched_token("tok"):
            with self.assertRaises(GitHubConnectorError) as context:
                transport.request(GitHubRequest(method="GET", path="/x"))
        self.assertEqual(context.exception.status, 0)
        self.assertIn("transport failure", context.exception.detail)

    def test_http_error_surfaces_status_and_not_the_credentials(self):
        outcome = urllib.error.HTTPError(
            "https://api.github.com/x", 503, "unavailable", None,
            io.BytesIO(b'{"message":"provider unavailable"}'),
        )
        transport, _ = make_transport(outcome)
        with _patched_token("tok-secret-123"):
            with self.assertRaises(GitHubConnectorError) as context:
                transport.request(GitHubRequest(method="GET", path="/x"))
        self.assertEqual(context.exception.status, 503)
        self.assertNotIn("tok-secret-123", str(context.exception))

    def test_connection_reset_is_wrapped_like_any_transport_failure(self):
        transport, _ = make_transport(ConnectionResetError(104, "connection reset"))
        with _patched_token("tok"):
            with self.assertRaises(GitHubConnectorError) as context:
                transport.request(GitHubRequest(method="GET", path="/x"))
        self.assertEqual(context.exception.status, 0)
        self.assertIn("ConnectionResetError", context.exception.detail)


# --------------------------------------------------------------------------
# Axis 9 — timeout handling (SEC-4)
# --------------------------------------------------------------------------


class TimeoutHandling(unittest.TestCase):
    """T-012 axis: timeout — bounded waits, wrapped errors, no retry storm."""

    def test_modern_timeout_error_is_wrapped_fail_closed(self):
        transport, _ = make_transport(TimeoutError("timed out"))
        with _patched_token("tok"):
            with self.assertRaises(GitHubConnectorError) as context:
                transport.request(GitHubRequest(method="GET", path="/x"))
        self.assertEqual(context.exception.status, 0)
        self.assertIn("TimeoutError", context.exception.detail)

    def test_timeout_is_bounded_and_configurable(self):
        default_transport = UrllibTransport()
        self.assertEqual(
            default_transport._timeout_seconds, 15  # noqa: SLF001
        )
        bounded, recording = make_transport(FakeHTTPResponse(), timeout_seconds=7)
        with _patched_token("tok"):
            bounded.request(GitHubRequest(method="GET", path="/x"))
        self.assertEqual(recording.calls[0]["timeout"], 7)

    def test_a_timed_out_request_is_never_retried_silently(self):
        transport, recording = make_transport(TimeoutError("timed out"))
        with _patched_token("tok"):
            with self.assertRaises(GitHubConnectorError):
                transport.request(GitHubRequest(method="GET", path="/x"))
        self.assertEqual(len(recording.calls), 1)  # one attempt, then surface


# --------------------------------------------------------------------------
# Axis 10 — error handling (SEC-5)
# --------------------------------------------------------------------------


class ErrorHandling(unittest.TestCase):
    """T-012 axis: error handling — typed, closed, non-inventive failures."""

    def test_non_json_success_body_fails_closed(self):
        connector = GitHubConnector(
            FakeTransport([make_response(200, "<html>not json</html>")])
        )
        with self.assertRaises(GitHubConnectorError) as context:
            connector.call("read_file", {"owner": "o", "repo": "r", "path": "p"})
        self.assertIn("non-JSON", context.exception.detail)

    def test_json_non_object_body_fails_closed(self):
        connector = GitHubConnector(FakeTransport([make_response(200, '["x"]')]))
        with self.assertRaises(GitHubConnectorError) as context:
            connector.call("read_file", {"owner": "o", "repo": "r", "path": "p"})
        self.assertIn("not an object", context.exception.detail)

    def test_empty_success_body_still_maps_to_empty_object(self):
        connector = GitHubConnector(FakeTransport([make_response(200, "  ")]))
        result = connector.call("read_file", {"owner": "o", "repo": "r", "path": "p"})
        self.assertEqual(result, {})

    def test_error_from_executor_surfaces_type_name_never_message(self):
        runtime, executor = _allowing_runtime_with_executor(
            "boom.tool", ValueError("internal note: payload-echo-77")
        )
        self.assertTrue(runtime)  # composition succeeds
        self.assertTrue(executor is not None)
        result = runtime.execute("a", "boom.tool", {})
        self.assertEqual(result.status, ERROR)
        self.assertEqual(result.error, "ValueError")
        self.assertNotIn("payload-echo-77", repr(result))


# --------------------------------------------------------------------------
# Local helpers
# --------------------------------------------------------------------------


def _allowing_runtime_with_executor(tool_id: str, failure: Exception):
    """Runtime with one ALLOW rule whose executor always raises ``failure``."""

    def explode(arguments: Any) -> Any:
        raise failure

    registry = ToolRegistry()
    runtime = Runtime(
        registry=registry,
        policy=PolicyGate([PolicyRule(tool_id=tool_id, decision=Decision.ALLOW)]),
    )
    runtime.register_contract(make_contract(name=tool_id))
    runtime.bind_executor(tool_id, explode)
    return runtime, explode


class _patched_token:
    """Context manager: run a block with GITHUB_TOKEN set to a fixed value."""

    def __init__(self, value: str) -> None:
        self._value = value
        self._patch = None

    def __enter__(self):
        from unittest import mock

        self._patch = mock.patch.dict(os.environ, {"GITHUB_TOKEN": self._value})
        return self._patch.__enter__()

    def __exit__(self, *exc: Any) -> Any:
        return self._patch.__exit__(*exc)


class _cleared_token_env:
    """Context manager: run a block with the token env var absent."""

    def __init__(self) -> None:
        self._patch = None

    def __enter__(self):
        from unittest import mock

        self._patch = mock.patch.dict(os.environ, {}, clear=True)
        return self._patch.__enter__()

    def __exit__(self, *exc: Any) -> Any:
        return self._patch.__exit__(*exc)


if __name__ == "__main__":
    unittest.main()
