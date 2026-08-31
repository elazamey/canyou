#!/usr/bin/env bash
#
# verify_adr.sh — architecture decision records exist and are well-formed.
#
# Every ADR under docs/decisions/ must carry Status (with an accepted state),
# Date, Context, and Decision sections. ADRs are governing records: appending
# a new ADR must not modify existing ones (AGENTS.md §4.9).

set -uo pipefail

failures=0

note_fail() {
  echo "FAIL adr: ${1}"
  failures=$((failures + 1))
}

adr_dir="docs/decisions"

if [[ ! -d "${adr_dir}" ]]; then
  note_fail "${adr_dir}/ does not exist"
  exit 1
fi

found=0
for adr in "${adr_dir}"/ADR-*.md; do
  [[ -e "${adr}" ]] || continue
  found=1
  ok=1
  grep -q "^- \*\*Status:\*\* ACCEPTED" "${adr}" || { note_fail "$(basename "${adr}"): missing 'Status: ACCEPTED'"; ok=0; }
  grep -q "^- \*\*Date:\*\*" "${adr}" || { note_fail "$(basename "${adr}"): missing Date"; ok=0; }
  grep -q "^## Context" "${adr}" || { note_fail "$(basename "${adr}"): missing '## Context'"; ok=0; }
  grep -q "^## Decision" "${adr}" || { note_fail "$(basename "${adr}"): missing '## Decision'"; ok=0; }
  grep -q "^## Alternatives considered" "${adr}" || { note_fail "$(basename "${adr}"): missing '## Alternatives considered'"; ok=0; }
  if [[ "${ok}" -eq 1 ]]; then
    echo "PASS adr: $(basename "${adr}") is well-formed"
  fi
done

if [[ "${found}" -eq 0 ]]; then
  note_fail "no ADR-*.md files found in ${adr_dir}/"
fi

if [[ "${failures}" -gt 0 ]]; then
  exit 1
fi
exit 0
