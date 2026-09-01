"""R-1 — Tool Registry with declared contracts.

Acceptance (verbatim from docs/REQUIREMENTS.md R-1): register a tool; look
it up by name (found, contract returned); enumerate (present); look up an
unknown name (NOT_FOUND, no crash).
"""

from __future__ import annotations

import unittest

from canyou.registry import (
    DuplicateToolError,
    RiskLevel,
    ToolContract,
    ToolNotFound,
    ToolRegistry,
)

from helpers import make_contract


class RegistryAcceptance(unittest.TestCase):
    def test_register_then_lookup_returns_contract(self):
        registry = ToolRegistry()
        declared = make_contract(name="github.read_file")
        registry.register(declared)
        looked_up = registry.lookup("github.read_file")
        self.assertIs(looked_up, declared)
        self.assertEqual(looked_up.permissions, ("test:use",))

    def test_enumerate_lists_registered_tools_sorted(self):
        registry = ToolRegistry()
        registry.register(make_contract(name="b.tool"))
        registry.register(make_contract(name="a.tool"))
        self.assertIn("a.tool", registry.tools())
        self.assertIn("b.tool", registry.tools())
        self.assertEqual(registry.tools(), ("a.tool", "b.tool"))

    def test_unknown_name_is_well_defined_not_found_without_crash(self):
        registry = ToolRegistry()
        with self.assertRaises(ToolNotFound) as context:
            registry.lookup("nope.tool")
        self.assertEqual(context.exception.tool_id, "nope.tool")

    def test_duplicate_registration_rejected(self):
        registry = ToolRegistry()
        registry.register(make_contract(name="same.tool"))
        with self.assertRaises(DuplicateToolError):
            registry.register(make_contract(name="same.tool"))


class ContractDeclaration(unittest.TestCase):
    def test_contract_requires_full_declaration(self):
        for broken in (
            {"name": ""},
            {"description": ""},
            {"permissions": ()},
            {"risk": "LOW"},
            {"audit_note": ""},
        ):
            fields = {
                "name": "n.tool",
                "description": "d",
                "permissions": ("p:one",),
                "risk": RiskLevel.LOW,
                "audit_note": "audit",
            }
            fields.update(broken)
            with self.assertRaises(ValueError, msg=f"fields={fields}"):
                ToolContract(**fields)


class RegistryHoldsContractsOnly(unittest.TestCase):
    def test_lookup_returns_a_contract_never_an_invocation_path(self):
        registry = ToolRegistry()
        registry.register(make_contract(name="echo.tool"))
        looked_up = registry.lookup("echo.tool")
        self.assertIsInstance(looked_up, ToolContract)
        self.assertFalse(callable(looked_up))
        public = [name for name in dir(ToolRegistry) if not name.startswith("_")]
        self.assertFalse(any("executor" in name for name in public))


if __name__ == "__main__":
    unittest.main()
