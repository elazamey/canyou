"""Connector layer — infrastructure adapters with no authority (R-3).

Exactly one connector implementation exists in the slice (R-3): the GitHub
adapter. Connectors execute requests that already passed the Policy Gate
and perform no authorization decisions of their own. They are reachable
only through the gated Runtime (R-4); the composition in ``canyou.runtime``
never hands a connector or a transport to callers.

``GitHubConnector`` is exposed through a lazy module attribute (PEP 562)
so the adapter module can do ``from . import Connector`` without a
circular import.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

__all__ = ("Connector", "GitHubConnector")


class Connector(ABC):
    """Interface implemented by every connector adapter (R-3)."""

    @abstractmethod
    def call(self, operation: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Execute one provider operation; raise on any failure (fail closed)."""


def __getattr__(name: str) -> Any:
    if name == "GitHubConnector":
        from .github import GitHubConnector

        return GitHubConnector
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
