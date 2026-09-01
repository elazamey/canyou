"""GitHub connector — the single Phase-1 adapter (R-3, directive section 7).

The transport is injected: behavioral tests run fully offline against a
fake transport (R-6), while production composition uses the stdlib
``urllib`` transport whose token is read from the environment at call
time and never stored, logged, or recorded in evidence (constraints
area 6).

Fail closed: a missing token, an unknown operation, a missing payload
field, or a non-2xx provider response raises. The connector never guesses,
never retries, and never performs an authorization decision of its own
(R-3) — authority lives exclusively in the Policy Gate.
"""

from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional

from . import Connector

_API_VERSION = "2022-11-28"
_USER_AGENT = "canyou-thin-slice"


class GitHubConnectorError(Exception):
    """Any connector-level failure; ``status`` 0 means no HTTP round trip."""

    def __init__(self, status: int, detail: str) -> None:
        super().__init__(f"github connector error (status={status}): {detail}")
        self.status = status
        self.detail = detail


class GitHubTokenMissing(GitHubConnectorError):
    """No token in the environment — refuse before any network attempt."""

    def __init__(self, token_env_var: str) -> None:
        super().__init__(
            status=0,
            detail=(
                f"environment variable {token_env_var} is not set; "
                "refusing to contact GitHub"
            ),
        )


@dataclass(frozen=True)
class GitHubRequest:
    """One provider HTTP request. Carries no credentials by design."""

    method: str
    path: str
    query: Optional[Dict[str, str]] = None
    body: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class GitHubResponse:
    """One provider HTTP response."""

    status: int
    body: str


class Transport(ABC):
    """Outbound HTTP interface; injectable so tests never touch a network."""

    @abstractmethod
    def request(self, request: GitHubRequest) -> GitHubResponse:
        """Perform one HTTP round trip."""


class UrllibTransport(Transport):
    """Stdlib transport — zero dependencies (ADR-0001, decision 2).

    The token is read from ``token_env_var`` at call time; it is never
    stored on the instance, never written into errors, and never logged.
    """

    def __init__(
        self,
        api_base: str = "https://api.github.com",
        token_env_var: str = "GITHUB_TOKEN",
        timeout_seconds: int = 15,
    ) -> None:
        self._api_base = api_base.rstrip("/")
        self._token_env_var = token_env_var
        self._timeout_seconds = timeout_seconds

    def request(self, request: GitHubRequest) -> GitHubResponse:
        token = os.environ.get(self._token_env_var)
        if not token:
            raise GitHubTokenMissing(self._token_env_var)
        url = self._api_base + request.path
        if request.query:
            url = url + "?" + urllib.parse.urlencode(request.query)
        data = None
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "User-Agent": _USER_AGENT,
            "X-GitHub-Api-Version": _API_VERSION,
        }
        if request.body is not None:
            data = json.dumps(request.body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        http_request = urllib.request.Request(
            url, data=data, headers=headers, method=request.method
        )
        try:
            with urllib.request.urlopen(
                http_request, timeout=self._timeout_seconds
            ) as response:
                return GitHubResponse(
                    status=response.status, body=response.read().decode("utf-8")
                )
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise GitHubConnectorError(status=exc.code, detail=detail[:200]) from None
        except urllib.error.URLError as exc:
            raise GitHubConnectorError(
                status=0, detail=f"transport failure: {exc.reason}"
            ) from None


class GitHubConnector(Connector):
    """The one Phase-1 connector (R-3). Surface fixed by ADR-0001:
    read file / create branch / commit file / create pull request.

    Holds no authority — it only maps gated operations to provider calls.
    """

    OPERATIONS = frozenset(
        {"read_file", "create_branch", "commit_file", "create_pull_request"}
    )

    def __init__(self, transport: Transport) -> None:
        self._transport = transport

    def call(self, operation: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Execute one provider operation; no authorization happens here."""
        if operation not in self.OPERATIONS:
            raise GitHubConnectorError(
                status=0, detail=f"unsupported operation: {operation}"
            )
        handlers = {
            "read_file": self._read_file,
            "create_branch": self._create_branch,
            "commit_file": self._commit_file,
            "create_pull_request": self._create_pull_request,
        }
        return handlers[operation](dict(payload))

    # -- transport plumbing --------------------------------------------------

    def _request(self, request: GitHubRequest) -> Dict[str, Any]:
        response = self._transport.request(request)
        if not 200 <= response.status < 300:
            raise GitHubConnectorError(
                status=response.status, detail=response.body[:200]
            )
        if not response.body.strip():
            return {}
        return json.loads(response.body)  # the provider contract is JSON

    def _request_optional(self, request: GitHubRequest) -> Optional[Dict[str, Any]]:
        """Like ``_request`` but tolerates 404 (returns None) — for lookups
        whose absence is a valid state (e.g. committing a brand-new file)."""
        response = self._transport.request(request)
        if response.status == 404:
            return None
        if not 200 <= response.status < 300:
            raise GitHubConnectorError(
                status=response.status, detail=response.body[:200]
            )
        return json.loads(response.body) if response.body.strip() else {}

    @staticmethod
    def _require(payload: Dict[str, Any], *keys: str) -> None:
        missing = [key for key in keys if not payload.get(key)]
        if missing:
            raise GitHubConnectorError(
                status=0, detail="missing required field(s): " + ", ".join(missing)
            )

    # -- operations ------------------------------------------------------------

    def _read_file(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self._require(payload, "owner", "repo", "path")
        query = {"ref": payload["ref"]} if payload.get("ref") else None
        path = "/repos/{0}/{1}/contents/{2}".format(
            payload["owner"],
            payload["repo"],
            urllib.parse.quote(payload["path"], safe="/"),
        )
        return self._request(GitHubRequest(method="GET", path=path, query=query))

    def _create_branch(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self._require(payload, "owner", "repo", "base", "branch")
        base = self._request(
            GitHubRequest(
                method="GET",
                path="/repos/{0}/{1}/git/ref/heads/{2}".format(
                    payload["owner"], payload["repo"], payload["base"]
                ),
            )
        )
        base_sha = base["object"]["sha"]
        created = self._request(
            GitHubRequest(
                method="POST",
                path="/repos/{0}/{1}/git/refs".format(
                    payload["owner"], payload["repo"]
                ),
                body={
                    "ref": "refs/heads/{0}".format(payload["branch"]),
                    "sha": base_sha,
                },
            )
        )
        return {"ref": created["ref"], "base_sha": base_sha}

    def _commit_file(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self._require(payload, "owner", "repo", "path", "branch", "message", "content")
        contents_path = "/repos/{0}/{1}/contents/{2}".format(
            payload["owner"],
            payload["repo"],
            urllib.parse.quote(payload["path"], safe="/"),
        )
        existing = self._request_optional(
            GitHubRequest(
                method="GET", path=contents_path, query={"ref": payload["branch"]}
            )
        )
        body: Dict[str, Any] = {
            "message": payload["message"],
            "branch": payload["branch"],
            "content": base64.b64encode(payload["content"].encode("utf-8")).decode(
                "ascii"
            ),
        }
        if existing is not None and existing.get("sha"):
            body["sha"] = existing["sha"]  # GitHub requires it when updating
        return self._request(GitHubRequest(method="PUT", path=contents_path, body=body))

    def _create_pull_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self._require(payload, "owner", "repo", "head", "base", "title")
        body: Dict[str, Any] = {
            "head": payload["head"],
            "base": payload["base"],
            "title": payload["title"],
        }
        if payload.get("body"):
            body["body"] = payload["body"]
        return self._request(
            GitHubRequest(
                method="POST",
                path="/repos/{0}/{1}/pulls".format(payload["owner"], payload["repo"]),
                body=body,
            )
        )
