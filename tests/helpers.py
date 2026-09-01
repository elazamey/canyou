"""Shared offline test helpers (R-6: no network anywhere in tests)."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple

from canyou.connectors.github import GitHubRequest, GitHubResponse, Transport
from canyou.registry import RiskLevel, ToolContract


class FakeTransport(Transport):
    """Replays queued responses offline and records every request."""

    def __init__(self, responses: Iterable[GitHubResponse] = ()) -> None:
        self.responses: List[GitHubResponse] = list(responses)
        self.requests: List[GitHubRequest] = []

    def request(self, request: GitHubRequest) -> GitHubResponse:
        self.requests.append(request)
        if not self.responses:
            raise AssertionError("FakeTransport ran out of queued responses")
        return self.responses.pop(0)


def make_contract(
    name: str = "echo.tool",
    risk: RiskLevel = RiskLevel.LOW,
    permissions: Tuple[str, ...] = ("test:use",),
) -> ToolContract:
    return ToolContract(
        name=name,
        description="test tool: " + name,
        permissions=permissions,
        risk=risk,
        audit_note="test audit note",
    )


def make_response(status: int, body: str) -> GitHubResponse:
    return GitHubResponse(status=status, body=body)


def assert_public_names_offenders(names: Iterable[str], forbidden: Iterable[str]) -> List[str]:
    """Return the forbidden words that appear inside any public name."""
    lowered = [name.lower() for name in names]
    return [word for word in forbidden if any(word in name for name in lowered)]


def require_keys(payload: Dict[str, Any], keys: Iterable[str]) -> None:
    """Tiny assertion helper for payload checks in tests."""
    for key in keys:
        assert key in payload, f"missing key in payload: {key}"
