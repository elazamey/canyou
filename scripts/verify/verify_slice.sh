#!/usr/bin/env bash
#
# verify_slice.sh — Phase-1 thin-slice gate (ADR-0001, decision 4).
#
# Runs entirely offline (R-6):
#   1. Python 3.11+ is available (fail closed when absent)
#   2. src/canyou byte-compiles
#   3. the package imports and exposes its public surface
#   4. the behavioral test suite passes (tests/, stdlib unittest)
#   5. negative control — a deliberately failing test run must FAIL,
#      proving this gate can actually detect failures (AGENTS.md lesson:
#      a check that cannot fail is not a check)
#
# Auto-discovered by verify.sh; the CI workflow is untouched by design.

set -uo pipefail

failures=0

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/../.." && pwd)"
cd "${repo_root}" || exit 1

note_fail() {
  echo "FAIL slice: ${1}"
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
echo "PASS slice: python3 >= 3.11 available ($(python3 --version 2>&1))"

# 2. Byte-compile the slice (compile/import check; __pycache__ is git-ignored).
if python3 -m compileall -q src/canyou; then
  echo "PASS slice: src/canyou byte-compiles"
else
  note_fail "src/canyou failed to byte-compile"
fi

# 3. Public-surface import check (defense in depth; fully asserted in tests).
if PYTHONPATH=src python3 -c 'import canyou; raise SystemExit(0 if canyou.__all__ else 1)'; then
  echo "PASS slice: canyou imports and exposes its public surface"
else
  note_fail "importing canyou or reading its public surface failed"
fi

# 4. Behavioral tests — offline, deterministic (R-6).
test_output="$(mktemp)"
if PYTHONPATH=src PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests \
  >"${test_output}" 2>&1; then
  echo "PASS slice: behavioral test suite (unittest) — $(grep -E '^Ran ' "${test_output}" | tail -1)"
else
  note_fail "behavioral test suite failed; output follows"
  sed 's/^/    /' "${test_output}"
fi
rm -f "${test_output}"

# 5. Negative control — the gate must be able to FAIL.
negative_dir="$(mktemp -d)"
trap 'rm -rf "${negative_dir}"' EXIT
printf '%s\n' \
  'from unittest import TestCase' \
  'class DeliberateFailure(TestCase):' \
  '    def test_must_fail(self):' \
  '        self.fail("negative control: this failure must be detected")' \
  > "${negative_dir}/test_deliberate_failure.py"
if PYTHONPATH=src python3 -m unittest discover -s "${negative_dir}" >/dev/null 2>&1; then
  note_fail "negative control unexpectedly PASSED — the gate cannot detect failures"
else
  echo "PASS slice: negative control fails as required (gate detects failures)"
fi

if [[ "${failures}" -gt 0 ]]; then
  exit 1
fi
exit 0
