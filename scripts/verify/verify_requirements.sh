#!/usr/bin/env bash
#
# verify_requirements.sh — requirements provenance discipline.
#
# The requirements file must exist, be an explicit draft (or signed), and every
# requirement must carry a Source line pointing at signed material only
# (docs/PRODUCT.md or docs/CONSTRAINTS.md) plus an Acceptance line.
# Enforces AGENTS.md §2: no requirement without an owner/source.

set -uo pipefail

failures=0

note_fail() {
  echo "FAIL requirements: ${1}"
  failures=$((failures + 1))
}

req_file="docs/REQUIREMENTS.md"

if [[ ! -s "${req_file}" ]]; then
  note_fail "${req_file} is missing or empty"
  exit 1
fi

# 1. Draft/signature status is explicit.
if grep -q "Status: DOCUMENTED — agent draft" "${req_file}" || grep -q "Owner signature:" "${req_file}"; then
  echo "PASS requirements: draft/signature status is explicit"
else
  note_fail "${req_file} must state its DOCUMENTED draft status and carry a signature block"
fi

# 2. Signature block must exist (empty until signed).
if grep -q "^## Signature block" "${req_file}"; then
  echo "PASS requirements: signature block present"
else
  note_fail "${req_file} is missing the '## Signature block' section"
fi

# 3. Every requirement block carries a Source line referencing signed material only.
bad_source="$(awk '
  /^### R-/ { if (id != "" && !has_source) print id; id = $2; has_source = 0; next }
  /^## /   { if (id != "" && !has_source) print id; id = ""; next }
  id != "" && /^- Source:/ && /docs\/(PRODUCT|CONSTRAINTS)\.md/ { has_source = 1 }
  END { if (id != "" && !has_source) print id }
' "${req_file}")"
if [[ -z "${bad_source}" ]]; then
  echo "PASS requirements: every requirement sources signed material (PRODUCT/CONSTRAINTS)"
else
  note_fail "requirements without a valid Source line:"
  printf '%s\n' "${bad_source}" | sed 's/^/    /'
fi

# 4. Every requirement block carries an Acceptance line.
bad_accept="$(awk '
  /^### R-/ { if (id != "" && !has_accept) print id; id = $2; has_accept = 0; next }
  /^## /   { if (id != "" && !has_accept) print id; id = ""; next }
  id != "" && /^- Acceptance:/ { has_accept = 1 }
  END { if (id != "" && !has_accept) print id }
' "${req_file}")"
if [[ -z "${bad_accept}" ]]; then
  echo "PASS requirements: every requirement has acceptance criteria"
else
  note_fail "requirements without an Acceptance line:"
  printf '%s\n' "${bad_accept}" | sed 's/^/    /'
fi

# 5. No requirement may source unsigned proposals.
if grep -q "^- Source:.*PROPOSALS" "${req_file}"; then
  note_fail "a requirement sources docs/PROPOSALS.md (unsigned) — not allowed"
else
  echo "PASS requirements: no requirement sources unsigned proposals"
fi

if [[ "${failures}" -gt 0 ]]; then
  exit 1
fi
exit 0
