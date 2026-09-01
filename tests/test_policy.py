"""R-2 — Policy Gate before every execution; default DENY.

Acceptance (verbatim from docs/REQUIREMENTS.md R-2): invoke an allowed tool
(executed); invoke a tool with a DENY policy (blocked, reason recorded);
invoke with no matching policy rule (DENY). Directive section 6 adds: a
destructive-class tool is never granted by default.
"""

from __future__ import annotations

import unittest

from canyou.policy import Decision, PolicyGate, PolicyRule
from canyou.registry import RiskLevel

from helpers import make_contract


class PolicyAcceptance(unittest.TestCase):
    def test_no_matching_rule_means_deny(self):
        gate = PolicyGate()
        outcome = gate.decide(make_contract(name="any.tool"))
        self.assertIs(outcome.decision, Decision.DENY)
        self.assertEqual(outcome.reason, "DEFAULT_DENY")

    def test_explicit_allow_rule_allows(self):
        gate = PolicyGate([PolicyRule(tool_id="a.tool", decision=Decision.ALLOW)])
        outcome = gate.decide(make_contract(name="a.tool"))
        self.assertIs(outcome.decision, Decision.ALLOW)
        self.assertEqual(outcome.reason, "EXPLICIT_ALLOW")

    def test_explicit_deny_blocks_with_recorded_reason(self):
        gate = PolicyGate([PolicyRule(tool_id="a.tool", decision=Decision.DENY)])
        outcome = gate.decide(make_contract(name="a.tool"))
        self.assertIs(outcome.decision, Decision.DENY)
        self.assertEqual(outcome.reason, "EXPLICIT_DENY")

    def test_deny_rule_beats_allow_rule(self):
        gate = PolicyGate(
            [
                PolicyRule(tool_id="a.tool", decision=Decision.ALLOW),
                PolicyRule(tool_id="a.tool", decision=Decision.DENY),
            ]
        )
        self.assertIs(gate.decide(make_contract(name="a.tool")).decision, Decision.DENY)

    def test_unknown_tool_is_denied(self):
        outcome = PolicyGate().decide(None)
        self.assertIs(outcome.decision, Decision.DENY)
        self.assertEqual(outcome.reason, "TOOL_NOT_REGISTERED")


class DestructiveBoundary(unittest.TestCase):
    def test_blocked_risk_denied_even_with_plain_allow_rule(self):
        destructive = make_contract(
            name="destroy.tool", risk=RiskLevel.BLOCKED, permissions=("repo:write",)
        )
        gate = PolicyGate([PolicyRule(tool_id="destroy.tool", decision=Decision.ALLOW)])
        outcome = gate.decide(destructive)
        self.assertIs(outcome.decision, Decision.DENY)
        self.assertEqual(outcome.reason, "DESTRUCTIVE_BLOCKED")

    def test_blocked_risk_allowed_only_by_explicit_enablement(self):
        destructive = make_contract(
            name="destroy.tool", risk=RiskLevel.BLOCKED, permissions=("repo:write",)
        )
        gate = PolicyGate(
            [
                PolicyRule(
                    tool_id="destroy.tool",
                    decision=Decision.ALLOW,
                    allows_destructive=True,
                )
            ]
        )
        self.assertIs(gate.decide(destructive).decision, Decision.ALLOW)

    def test_medium_risk_tool_runs_with_plain_allow(self):
        gate = PolicyGate([PolicyRule(tool_id="m.tool", decision=Decision.ALLOW)])
        outcome = gate.decide(
            make_contract(name="m.tool", risk=RiskLevel.MEDIUM, permissions=("w",))
        )
        self.assertIs(outcome.decision, Decision.ALLOW)


if __name__ == "__main__":
    unittest.main()
