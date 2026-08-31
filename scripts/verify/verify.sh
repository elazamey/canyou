#!/usr/bin/env bash
#
# verify.sh — single entry point for deterministic repository verification.
#
# Runs every verify_*.sh script located next to this file and prints a summary.
# Exit code 0 = every check passed; 1 = at least one failure.
# Requirements: bash + coreutils only. No network, no randomness.
#
# Usage: bash scripts/verify/verify.sh

set -uo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/../.." && pwd)"

cd "${repo_root}" || exit 1

overall=0
run=0

echo "=============================================================="
echo " canyou repository verification"
echo " entry: scripts/verify/verify.sh"
echo "=============================================================="

found_any=0
for check in "${script_dir}"/verify_*.sh; do
  if [[ ! -e "${check}" ]]; then
    echo "FAIL verify: no verify_*.sh scripts found in ${script_dir}"
    overall=1
    break
  fi
  found_any=1
  run=$((run + 1))
  echo
  echo "--- Running: $(basename "${check}")"
  echo "--------------------------------------------------------------"
  if bash "${check}"; then
    echo ">>> $(basename "${check}"): PASS"
  else
    echo ">>> $(basename "${check}"): FAIL"
    overall=1
  fi
done

if [[ "${found_any}" -eq 0 ]]; then
  run=0
fi

echo
echo "=============================================================="
if [[ "${overall}" -eq 0 ]]; then
  echo " RESULT: PASS — ${run} check group(s). Repository state matches its contract."
else
  echo " RESULT: FAIL — fix the failures above before committing (AGENTS.md §5)."
fi
echo "=============================================================="

exit "${overall}"
