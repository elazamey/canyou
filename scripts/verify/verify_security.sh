#!/usr/bin/env bash
#
# verify_security.sh — T-012 Security Gate: deterministic harness.
#
# Runs entirely offline (R-6), bash + coreutils + python3 only:
#   1. Python 3.11+ available (same runtime contract as ADR-0001)
#   2. application and test code byte-compiles
#   3. the security test module runs green (tests/test_security_gate.py)
#   4. negative control — a deliberately failing test must FAIL this gate
#      (AGENTS.md lesson: a check that cannot fail is not a check)
#   5. axis coverage — each of the ten T-012 axes has a named test class
#   6. static invariants — exactly one permission-ceiling definition, no
#      print/logging in the connector, https-only provider base
#
# Auto-discovered by verify.sh; the CI workflow is untouched by design
# (the workflows-permission constraint documented in tasks/CURRENT.md).

set -uo pipefail

failures=0

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/../.." && pwd)"
cd "${repo_root}" || exit 1

note_fail() {
  echo "FAIL security: ${1}"
  failures=$((failures + 1))
}

# 1. Python 3.11+ available — fail closed (ADR-0001: Python 3.11+ runtime).
if ! command -v python3 >/dev/null 2>&1; then
  note_fail "python3 is required but was not found in PATH"
  exit 1
fi
if ! python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)'; then
  note_fail "python3 >= 3.11 is required (ADR-0001); found: $(python3 --version 2>&1)"
  exit 1
fi
echo "PASS security: python3 >= 3.11 available ($(python3 --version 2>&1))"

# 2. Byte-compile application and tests (compile check; __pycache__ ignored).
if python3 -m compileall -q src/canyou tests; then
  echo "PASS security: src/canyou and tests byte-compile"
else
  note_fail "src/canyou or tests failed to byte-compile"
fi

# 3. Security harness — the T-012 behavioral tests, all offline (R-6).
test_output="$(mktemp)"
if PYTHONPATH=src PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests \
  -p 'test_security_*.py' >"${test_output}" 2>&1; then
  echo "PASS security: security harness (unittest) — $(grep -E '^Ran ' "${test_output}" | tail -1)"
else
  note_fail "security harness failed; output follows"
  sed 's/^/    /' "${test_output}"
fi
rm -f "${test_output}"

# 4. Negative control — the gate must be able to FAIL.
negative_dir="$(mktemp -d)"
trap 'rm -rf "${negative_dir}"' EXIT
printf '%s\n' \
  'from unittest import TestCase' \
  'class DeliberateFailure(TestCase):' \
  '    def test_must_fail(self):' \
  '        self.fail("negative control: this failure must be detected")' \
  > "${negative_dir}/test_security_negative_control.py"
if PYTHONPATH=src python3 -m unittest discover -s "${negative_dir}" \
  -p 'test_security_*.py' >/dev/null 2>&1; then
  note_fail "negative control unexpectedly PASSED — the security gate cannot detect failures"
else
  echo "PASS security: negative control fails as required (gate detects failures)"
fi

# 5. Axis coverage — the ten axes of T-012 each carry a named test class;
#    a silently dropped axis makes this gate FAIL instead of passing unseen.
axes_ok=1
for axis in \
  Authentication Authorization LeastPrivilege SecretsHandling ConnectorIsolation \
  PolicyBypassResistance EvidenceIntegrity NetworkFailure TimeoutHandling ErrorHandling; do
  if ! grep -q "^class ${axis}(unittest.TestCase):" tests/test_security_gate.py; then
    note_fail "axis '${axis}' is missing its test class in tests/test_security_gate.py"
    axes_ok=0
  fi
done
if [[ "${axes_ok}" -eq 1 ]]; then
  echo "PASS security: all ten T-012 axes carry named test classes"
fi

# 6. Static invariants of the security surface (SEC-2/SEC-4 guards).
invariants_ok=1
ceiling_defs="$(grep -rn --include='*.py' -e '^PHASE1_PERMISSIONS' src/canyou | wc -l)"
if [[ "${ceiling_defs}" -ne 1 ]]; then
  note_fail "PHASE1_PERMISSIONS must be defined exactly once in src/canyou (found ${ceiling_defs})"
  invariants_ok=0
fi
if grep -nE 'print\(|logging\.' src/canyou/connectors/github.py >/dev/null 2>&1; then
  note_fail "print/logging call in src/canyou/connectors/github.py — the connector must never emit credential-bearing output"
  invariants_ok=0
fi
if grep -n 'http://' src/canyou/connectors/github.py >/dev/null 2>&1; then
  note_fail "cleartext http:// reference in src/canyou/connectors/github.py — the provider base is https-only"
  invariants_ok=0
fi
if [[ "${invariants_ok}" -eq 1 ]]; then
  echo "PASS security: static invariants hold (single permission ceiling; no print/logging in connector; https-only provider base)"
fi

if [[ "${failures}" -gt 0 ]]; then
  exit 1
fi
exit 0
