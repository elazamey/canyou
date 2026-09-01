"""Policy Gate — renders an ALLOW/DENY decision BEFORE any execution (R-2).

Secure default: when no rule matches, the outcome is DENY. An explicit DENY
rule always wins over an ALLOW rule (fail closed). A tool whose contract
declares ``RiskLevel.BLOCKED`` (the destructive class) stays DENY unless the
matching ALLOW rule explicitly sets ``allows_destructive=True`` — destructive
capability is never granted by default (ADR-0001, directive section 6).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, List, Tuple

from .registry import RiskLevel, ToolContract


class Decision(Enum):
    """The only two outcomes the Gate can render."""

    ALLOW = "ALLOW"
    DENY = "DENY"


@dataclass(frozen=True)
class PolicyRule:
    """One explicit policy entry; ``decision`` is ALLOW or DENY."""

    tool_id: str
    decision: Decision
    allows_destructive: bool = False
    detail: str = ""

    def __post_init__(self) -> None:
        if not self.tool_id:
            raise ValueError("policy rule requires a non-empty tool_id")


@dataclass(frozen=True)
class PolicyDecision:
    """Gate outcome: decision plus a machine-readable reason (R-2)."""

    decision: Decision
    reason: str
    detail: str = ""


class PolicyGate:
    """Default-DENY gate; the only authority for execution decisions."""

    def __init__(self, rules: Iterable[PolicyRule] = ()) -> None:
        self._rules: Tuple[PolicyRule, ...] = tuple(rules)

    def decide(self, contract: ToolContract | None) -> PolicyDecision:
        """Decide for one invocation attempt; DENY when nothing matches."""
        if contract is None:
            return PolicyDecision(
                decision=Decision.DENY,
                reason="TOOL_NOT_REGISTERED",
                detail="no declared contract exists for the requested tool",
            )
        matching: List[PolicyRule] = [r for r in self._rules if r.tool_id == contract.name]
        for rule in matching:  # explicit DENY wins — fail closed (R-2)
            if rule.decision is Decision.DENY:
                return PolicyDecision(
                    decision=Decision.DENY,
                    reason="EXPLICIT_DENY",
                    detail=rule.detail or "denied by explicit policy rule",
                )
        allow_rules = [r for r in matching if r.decision is Decision.ALLOW]
        if not allow_rules:
            return PolicyDecision(  # secure default (R-2)
                decision=Decision.DENY,
                reason="DEFAULT_DENY",
                detail="no matching policy rule; the default is DENY",
            )
        rule = allow_rules[0]
        if contract.risk is RiskLevel.BLOCKED and not rule.allows_destructive:
            return PolicyDecision(
                decision=Decision.DENY,
                reason="DESTRUCTIVE_BLOCKED",
                detail="destructive-class tool requires an explicitly enabling rule",
            )
        return PolicyDecision(
            decision=Decision.ALLOW,
            reason="EXPLICIT_ALLOW",
            detail=rule.detail or "allowed by explicit policy rule",
        )
