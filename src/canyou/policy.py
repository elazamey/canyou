"""Policy Gate — renders an ALLOW/DENY decision BEFORE any execution (R-2).

Secure default: when no rule matches, the outcome is DENY. An explicit DENY
rule always wins over an ALLOW rule (fail closed). A tool whose contract
declares ``RiskLevel.BLOCKED`` (the destructive class) stays DENY unless the
matching ALLOW rule explicitly sets ``allows_destructive=True`` — destructive
capability is never granted by default (ADR-0001, directive section 6).

Security-Gate hardening (T-012), both fail closed:

- SEC-1 (authorization): a contract that declares ``requires_approval=True``
  can never be satisfied in Phase 1 — approval workflows beyond the DENY
  default are an explicit non-goal (R-7) — so the gate DENYs instead of
  silently ignoring the declared requirement (``APPROVAL_REQUIRED``).
- SEC-2 (least privilege): a gate may be constructed with a
  ``permission_ceiling`` — the closed set of permission names this phase may
  ever confer. Any ALLOW candidate whose contract declares a name outside
  the ceiling is DENYed with ``UNKNOWN_PERMISSION`` (grant or declaration
  outside the ceiling is rejected, never silently conferred). The generic
  gate stays ceiling-agnostic; the Phase-1 GitHub composition wires
  :data:`PHASE1_PERMISSIONS` in (see ``canyou.runtime.build_github_runtime``).

Deny-reason precedence is fixed and deterministic: ``TOOL_NOT_REGISTERED``
> ``EXPLICIT_DENY`` > ``DEFAULT_DENY`` > ``DESTRUCTIVE_BLOCKED`` >
``APPROVAL_REQUIRED`` > ``UNKNOWN_PERMISSION``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet, Iterable, List, Optional, Tuple

from .registry import RiskLevel, ToolContract

# SEC-2: the Phase-1 permission ceiling — the only permission names this
# phase's tools may declare or be granted. Extending the slice's authority
# (e.g. an issue-writing operation needing ``issues:write``) means naming it
# here explicitly, in code review, plus the connector operation, the declared
# contract, and the accept/reject tests. Single source; never infer it.
PHASE1_PERMISSIONS: FrozenSet[str] = frozenset(
    {"repo:read", "repo:write", "pr:create"}
)


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
    """Default-DENY gate; the only authority for execution decisions.

    ``permission_ceiling`` (SEC-2): when given, an ALLOW candidate whose
    contract declares any permission outside this closed set is DENYed with
    ``UNKNOWN_PERMISSION``. When omitted (the plain gate), no ceiling is
    applied — ceilings are a composition-time posture, so generic/test
    registries keep their declared names (no breakage of non-Phase-1 tools).
    """

    def __init__(
        self,
        rules: Iterable[PolicyRule] = (),
        permission_ceiling: Optional[Iterable[str]] = None,
    ) -> None:
        self._rules: Tuple[PolicyRule, ...] = tuple(rules)
        self._permission_ceiling: Optional[FrozenSet[str]] = (
            frozenset(permission_ceiling) if permission_ceiling is not None else None
        )

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
        if contract.requires_approval:  # SEC-1: never silently ignore it
            return PolicyDecision(
                decision=Decision.DENY,
                reason="APPROVAL_REQUIRED",
                detail=(
                    "contract declares an approval requirement that Phase-1 "
                    "cannot satisfy (approval workflows beyond the DENY "
                    "default are out of scope, R-7); failing closed"
                ),
            )
        if self._permission_ceiling is not None:  # SEC-2: least privilege
            unknown = sorted(set(contract.permissions) - self._permission_ceiling)
            if unknown:
                return PolicyDecision(
                    decision=Decision.DENY,
                    reason="UNKNOWN_PERMISSION",
                    detail=(
                        "declared permission(s) outside the policy ceiling: "
                        + ", ".join(unknown)
                    ),
                )
        return PolicyDecision(
            decision=Decision.ALLOW,
            reason="EXPLICIT_ALLOW",
            detail=rule.detail or "allowed by explicit policy rule",
        )
