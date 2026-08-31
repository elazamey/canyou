#!/usr/bin/env bash
#
# verify_content.sh — governance content rules.
#
# Checks that the contract, state files, and changelog say what they must:
# full state vocabulary, required sections, disciplined status rows.

set -uo pipefail

failures=0

note_fail() {
  echo "FAIL content: ${1}"
  failures=$((failures + 1))
}

# 1. AGENTS.md defines the full state vocabulary.
vocab_ok=1
for state in DOCUMENTED IMPLEMENTED VERIFIED COMMITTED HANDOFF_READY; do
  if ! grep -q "${state}" AGENTS.md; then
    echo "FAIL content: AGENTS.md does not mention state ${state}"
    vocab_ok=0
  fi
done
if [[ "${vocab_ok}" -eq 1 ]]; then
  echo "PASS content: AGENTS.md defines the full state vocabulary"
fi

# 2. AGENTS.md states the source-of-truth rule.
if grep -qi "single source of truth" AGENTS.md; then
  echo "PASS content: AGENTS.md states the source-of-truth rule"
else
  note_fail "AGENTS.md must state that the repository is the single source of truth"
fi

# 3. CHANGELOG.md keeps an Unreleased section.
if grep -q "^## \[Unreleased\]" CHANGELOG.md; then
  echo "PASS content: CHANGELOG.md has an [Unreleased] section"
else
  note_fail "CHANGELOG.md is missing '## [Unreleased]'"
fi

# 4. tasks/CURRENT.md has all required sections.
for section in "## Active Task" "## Status Board" "## Verified Facts" "## Open Questions" "## Next Actions"; do
  if grep -q "^${section}\$" tasks/CURRENT.md; then
    echo "PASS content: tasks/CURRENT.md has '${section}'"
  else
    note_fail "tasks/CURRENT.md is missing '${section}'"
  fi
done

# 5. Every Status Board row carries exactly one allowed state.
bad_rows="$(awk '
  /^## Status Board/ { in_board = 1; next }
  /^## / { in_board = 0 }
  in_board && /^\|/ &&
  $0 !~ /^\|[[:space:]]*[-: ]+\|/ &&
  $0 !~ /^\|[[:space:]]*Item/ {
    if ($0 !~ /DOCUMENTED|IMPLEMENTED|VERIFIED|COMMITTED|HANDOFF_READY/) print
  }
' tasks/CURRENT.md)"
if [[ -z "${bad_rows}" ]]; then
  echo "PASS content: every Status Board row carries an allowed state"
else
  note_fail "Status Board rows without an allowed state:"
  printf '%s\n' "${bad_rows}" | sed 's/^/    /'
fi

# 6. docs/HANDOFF.md defines the protocol and keeps a records section.
for marker in "## Record template" "## Latest handoff records"; do
  if grep -q "^${marker}\$" docs/HANDOFF.md; then
    echo "PASS content: docs/HANDOFF.md has '${marker}'"
  else
    note_fail "docs/HANDOFF.md is missing '${marker}'"
  fi
done

# 7. tasks/BACKLOG.md keeps a backlog table.
if grep -q "^## Backlog\$" tasks/BACKLOG.md; then
  echo "PASS content: tasks/BACKLOG.md has a '## Backlog' table"
else
  note_fail "tasks/BACKLOG.md is missing '## Backlog'"
fi

if [[ "${failures}" -gt 0 ]]; then
  exit 1
fi
exit 0
