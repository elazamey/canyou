"""R-5 + directive section 8 — minimal auditable record, append-only.

Acceptance (verbatim from docs/REQUIREMENTS.md R-5): after the R-2
scenarios, exactly one record per attempt exists with the four required
fields; records cannot be modified through public interfaces.
"""

from __future__ import annotations

import dataclasses
import json
import unittest

from canyou.evidence import EvidenceLog, TraceRecord, reference_of


def make_record(**overrides):
    fields = dict(
        execution_id="exec-1",
        agent_id="agent-1",
        tool_id="github.read_file",
        timestamp="2026-09-01T00:00:00+00:00",
        policy_decision="ALLOW",
        policy_reason="EXPLICIT_ALLOW",
        input_reference="in-ref",
        output_reference="out-ref",
    )
    fields.update(overrides)
    return TraceRecord(**fields)


class RecordShape(unittest.TestCase):
    def test_record_carries_required_fields(self):
        trace = make_record()
        self.assertEqual(trace.tool_id, "github.read_file")  # R-5
        self.assertEqual(trace.policy_decision, "ALLOW")  # R-5
        self.assertEqual(trace.policy_reason, "EXPLICIT_ALLOW")  # R-2 machine-readable
        self.assertEqual(trace.timestamp, "2026-09-01T00:00:00+00:00")  # R-5
        self.assertEqual(trace.execution_id, "exec-1")  # directive section 8
        self.assertEqual(trace.agent_id, "agent-1")  # directive section 8
        self.assertTrue(trace.input_reference)  # directive section 8 reference
        self.assertTrue(trace.output_reference)  # directive section 8 reference
        self.assertIsNone(trace.artifact_reference)  # optional per section 8

    def test_records_are_immutable(self):
        trace = make_record()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            trace.tool_id = "tampered.tool"


class AppendOnlyBehavior(unittest.TestCase):
    def test_append_then_read_back_in_order(self):
        log = EvidenceLog()
        log.append(make_record(execution_id="e1"))
        log.append(make_record(execution_id="e2"))
        self.assertEqual([r.execution_id for r in log.records()], ["e1", "e2"])
        self.assertEqual(len(log), 2)

    def test_snapshot_cannot_mutate_the_log(self):
        log = EvidenceLog()
        log.append(make_record())
        snapshot = log.records()
        with self.assertRaises(AttributeError):
            snapshot.append(make_record())  # tuple: no append
        self.assertEqual(len(log), 1)

    def test_records_enter_only_as_trace_records(self):
        log = EvidenceLog()
        with self.assertRaises(TypeError):
            log.append({"execution_id": "forged"})

    def test_no_public_mutation_api_exists(self):
        forbidden = ("delete", "remove", "update", "clear", "pop", "discard")
        public = [name for name in dir(EvidenceLog) if not name.startswith("_")]
        offenders = [
            name for name in public if any(word in name.lower() for word in forbidden)
        ]
        self.assertEqual(offenders, [])


class References(unittest.TestCase):
    def test_reference_is_deterministic_content_hash(self):
        self.assertEqual(reference_of({"a": 1}), reference_of({"a": 1}))
        self.assertNotEqual(reference_of({"a": 1}), reference_of({"a": 2}))
        self.assertEqual(len(reference_of({"a": 1})), 64)

    def test_secrets_never_reach_evidence(self):
        secret = "super-secret-value-42"
        payload = {"tool_id": "t.tool", "arguments": {"token": secret}}
        log = EvidenceLog()
        log.append(
            make_record(
                input_reference=reference_of(payload),
                output_reference=reference_of({"outcome": "DENIED"}),
            )
        )
        lines = log.to_json_lines()
        self.assertNotIn(secret, lines)
        self.assertIn(reference_of(payload), lines)

    def test_json_lines_shape_is_deterministic(self):
        log = EvidenceLog()
        log.append(make_record())
        parsed = json.loads(log.to_json_lines())
        self.assertEqual(parsed["tool_id"], "github.read_file")
        self.assertEqual(parsed["policy_decision"], "ALLOW")
        self.assertEqual(
            log.to_json_lines(),
            "\n".join([log.to_json_lines().splitlines()[0]]),
        )


if __name__ == "__main__":
    unittest.main()
