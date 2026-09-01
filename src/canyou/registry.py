"""Tool Registry — declared contracts and name-based discovery (R-1).

The registry holds *contracts only*. Executors are bound privately in the
Runtime (``canyou.runtime.Runtime.bind_executor``), so a registry lookup
can never yield an invocation path that skips the Policy Gate (R-4). A
lookup of an unknown name raises :class:`ToolNotFound` — the well-defined
NOT_FOUND outcome required by R-1, never undefined behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Tuple


class RiskLevel(Enum):
    """Declared risk of a tool's operation (directive section 6 / ADR-0001)."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    BLOCKED = "BLOCKED"  # destructive class: never enabled by default


@dataclass(frozen=True)
class ToolContract:
    """The declaration every tool must carry (directive section 6 / R-1)."""

    name: str
    description: str
    permissions: Tuple[str, ...]
    risk: RiskLevel
    requires_approval: bool = False
    audit_note: str = ""

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("tool contract requires a non-empty name")
        if not self.description:
            raise ValueError("tool contract requires a non-empty description")
        if not self.permissions:
            raise ValueError(
                "tool contract must declare at least one permission (least privilege)"
            )
        if not isinstance(self.risk, RiskLevel):
            raise ValueError("tool contract risk must be a RiskLevel value")
        if not self.audit_note:
            raise ValueError("tool contract must declare audit information")


class DuplicateToolError(Exception):
    """Raised when registering a name that is already registered."""


class ToolNotFound(LookupError):
    """Well-defined NOT_FOUND outcome for unknown tool names (R-1)."""

    def __init__(self, tool_id: str) -> None:
        super().__init__(f"tool not registered: {tool_id}")
        self.tool_id = tool_id


class ToolRegistry:
    """Name-indexed store of declared contracts (R-1)."""

    def __init__(self) -> None:
        self._contracts: Dict[str, ToolContract] = {}

    def register(self, contract: ToolContract) -> None:
        """Register a declared contract; rejects duplicate names."""
        if contract.name in self._contracts:
            raise DuplicateToolError(contract.name)
        self._contracts[contract.name] = contract

    def lookup(self, tool_id: str) -> ToolContract:
        """Return the contract for ``tool_id`` or raise ToolNotFound (R-1)."""
        try:
            return self._contracts[tool_id]
        except KeyError:
            raise ToolNotFound(tool_id) from None

    def has(self, tool_id: str) -> bool:
        """Return True when a contract with this name is registered."""
        return tool_id in self._contracts

    def tools(self) -> Tuple[str, ...]:
        """Enumerate registered tool names, sorted for determinism (R-1)."""
        return tuple(sorted(self._contracts))

    def __contains__(self, tool_id: object) -> bool:
        return tool_id in self._contracts

    def __len__(self) -> int:
        return len(self._contracts)
