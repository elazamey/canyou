"""R-3/R-7 — structural surface: exactly one connector; non-goals absent.

R-3 acceptance (verbatim): the slice exposes exactly one connector
implementation. R-7 acceptance: the slice's public surface introduces none
of the excluded components (structural review against the slice definition).
"""

from __future__ import annotations

import unittest
from pathlib import Path

import canyou
import canyou.connectors
from canyou.connectors import Connector, GitHubConnector


class ExactlyOneConnector(unittest.TestCase):
    def test_single_connector_implementation_exists(self):
        self.assertEqual(Connector.__subclasses__(), [GitHubConnector])

    def test_connector_module_exports_interface_plus_one_adapter(self):
        self.assertEqual(set(canyou.connectors.__all__), {"Connector", "GitHubConnector"})


class NonGoalsAbsent(unittest.TestCase):
    NON_GOAL_TOKENS = (
        "ledger",
        "meter",
        "billing",
        "memory",
        "model",
        "router",
        "provider",
        "multi_agent",
        "multiagent",
        "marketplace",
        "vercel",
        "cloudflare",
        "approval_workflow",
    )

    def test_exported_names_contain_no_non_goal_components(self):
        exported = " ".join(canyou.__all__).lower()
        offenders = [token for token in self.NON_GOAL_TOKENS if token in exported]
        self.assertEqual(offenders, [])


class SliceLayout(unittest.TestCase):
    def test_slice_files_exist_exactly_as_architected(self):
        """ADR-0001 layout: registry / policy / connectors+github / evidence /
        runtime — and nothing else on the application surface."""
        base = Path(canyou.__file__).parent
        expected = {
            "__init__.py",
            "registry.py",
            "policy.py",
            "evidence.py",
            "runtime.py",
            "connectors/__init__.py",
            "connectors/github.py",
        }
        actual = {
            str(path.relative_to(base)) for path in base.rglob("*.py")
        }
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
