"""R-3/R-6 — GitHub connector: the one adapter, offline, fail closed.

R-3 acceptance (verbatim): the slice exposes exactly one connector
implementation. R-6 acceptance: checks run offline — every test here uses
an injected fake transport; no test touches a network.
"""

from __future__ import annotations

import os
import unittest
from unittest import mock

from canyou.connectors import Connector, GitHubConnector
from canyou.connectors.github import (
    GitHubConnectorError,
    GitHubRequest,
    GitHubResponse,
    UrllibTransport,
)

from helpers import FakeTransport, make_response


class OfflineOperations(unittest.TestCase):
    def test_read_file_builds_get_contents_request(self):
        transport = FakeTransport(
            [make_response(200, '{"name":"f.txt","sha":"abc"}')]
        )
        connector = GitHubConnector(transport)
        result = connector.call(
            "read_file",
            {"owner": "o", "repo": "r", "path": "docs/x.md", "ref": "main"},
        )
        self.assertEqual(result["sha"], "abc")
        sent = transport.requests[0]
        self.assertEqual(sent.method, "GET")
        self.assertEqual(sent.path, "/repos/o/r/contents/docs/x.md")
        self.assertEqual(sent.query, {"ref": "main"})

    def test_create_branch_reads_base_then_posts_ref(self):
        transport = FakeTransport(
            [
                make_response(200, '{"object":{"sha":"basesha"}}'),
                make_response(201, '{"ref":"refs/heads/feature"}'),
            ]
        )
        result = GitHubConnector(transport).call(
            "create_branch",
            {"owner": "o", "repo": "r", "base": "main", "branch": "feature"},
        )
        self.assertEqual(result, {"ref": "refs/heads/feature", "base_sha": "basesha"})
        post = transport.requests[1]
        self.assertEqual(post.method, "POST")
        self.assertEqual(
            post.body, {"ref": "refs/heads/feature", "sha": "basesha"}
        )

    def test_commit_file_updates_with_existing_sha(self):
        transport = FakeTransport(
            [
                make_response(200, '{"sha":"oldsha"}'),
                make_response(201, '{"commit":{"sha":"newsha"}}'),
            ]
        )
        GitHubConnector(transport).call(
            "commit_file",
            {
                "owner": "o",
                "repo": "r",
                "path": "f.txt",
                "branch": "main",
                "message": "m",
                "content": "hi",
            },
        )
        put = transport.requests[1]
        self.assertEqual(put.method, "PUT")
        self.assertEqual(put.body["sha"], "oldsha")
        self.assertEqual(put.body["branch"], "main")
        self.assertEqual(put.body["content"], "aGk=")  # base64 of "hi"

    def test_commit_file_new_file_has_no_sha(self):
        transport = FakeTransport(
            [
                make_response(404, '{"message":"Not Found"}'),
                make_response(201, '{"commit":{"sha":"newsha"}}'),
            ]
        )
        GitHubConnector(transport).call(
            "commit_file",
            {
                "owner": "o",
                "repo": "r",
                "path": "new.txt",
                "branch": "main",
                "message": "m",
                "content": "hi",
            },
        )
        self.assertNotIn("sha", transport.requests[1].body)

    def test_create_pull_request_posts_to_pulls(self):
        transport = FakeTransport([make_response(201, '{"number":7}')])
        result = GitHubConnector(transport).call(
            "create_pull_request",
            {"owner": "o", "repo": "r", "head": "feature", "base": "main", "title": "t"},
        )
        self.assertEqual(result["number"], 7)
        self.assertEqual(transport.requests[0].path, "/repos/o/r/pulls")


class FailClosed(unittest.TestCase):
    def test_unknown_operation_rejected_without_requests(self):
        transport = FakeTransport()
        connector = GitHubConnector(transport)
        with self.assertRaises(GitHubConnectorError):
            connector.call("delete_repository", {})
        self.assertEqual(transport.requests, [])

    def test_missing_payload_field_rejected(self):
        connector = GitHubConnector(FakeTransport())
        with self.assertRaises(GitHubConnectorError):
            connector.call("read_file", {"owner": "o"})

    def test_non_2xx_response_raises_with_status(self):
        connector = GitHubConnector(
            FakeTransport([make_response(422, '{"message":"bad"}')])
        )
        with self.assertRaises(GitHubConnectorError) as context:
            connector.call("read_file", {"owner": "o", "repo": "r", "path": "p"})
        self.assertEqual(context.exception.status, 422)

    def test_missing_token_fails_before_any_network_attempt(self):
        transport = UrllibTransport(api_base="https://api.github.invalid")
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(GitHubConnectorError):
                transport.request(GitHubRequest(method="GET", path="/x"))

    def test_urllib_transport_never_stores_the_token(self):
        with mock.patch.dict(os.environ, {"GITHUB_TOKEN": "tok-secret-123"}):
            transport = UrllibTransport()
            self.assertNotIn("tok-secret-123", repr(vars(transport)))

    def test_connector_instance_never_holds_credentials(self):
        transport = FakeTransport([make_response(200, "{}")])
        connector = GitHubConnector(transport)
        with mock.patch.dict(os.environ, {"GITHUB_TOKEN": "tok-secret-123"}):
            connector.call("read_file", {"owner": "o", "repo": "r", "path": "p"})
        self.assertNotIn("tok-secret-123", repr(vars(connector)))
        self.assertNotIn("tok-secret-123", repr(transport.requests))


if __name__ == "__main__":
    unittest.main()
