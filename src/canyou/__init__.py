"""canyou — Phase-1 thin slice (ADR-0001).

Public surface: Tool Registry with declared contracts, the default-DENY
Policy Gate, append-only Evidence, and the gated Runtime. Exactly one
connector exists (R-3) and it is reachable only through the gated Runtime
(R-4). None of the R-7 non-goals (ledger, metering, memory, model/router,
UI, extra connectors) appear on this surface.
"""

from __future__ import annotations

from .evidence import EvidenceLog, TraceRecord
from .policy import Decision, PolicyDecision, PolicyGate, PolicyRule
from .registry import (
    DuplicateToolError,
    RiskLevel,
    ToolContract,
    ToolNotFound,
    ToolRegistry,
)
from .runtime import (
    DENIED,
    ERROR,
    EXECUTED,
    NOT_FOUND,
    ExecutionResult,
    Runtime,
    build_github_runtime,
)

__all__ = (
    "DENIED",
    "Decision",
    "DuplicateToolError",
    "ERROR",
    "EXECUTED",
    "EvidenceLog",
    "ExecutionResult",
    "NOT_FOUND",
    "PolicyDecision",
    "PolicyGate",
    "PolicyRule",
    "RiskLevel",
    "Runtime",
    "ToolContract",
    "ToolNotFound",
    "ToolRegistry",
    "TraceRecord",
    "build_github_runtime",
)
