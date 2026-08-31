#!/usr/bin/env bash
#
# verify_structure.sh — the governance structure is complete.
#
# Fails when any required file is missing or empty, or when the
# verification entry point is not executable.

set -uo pipefail

failures=0

required_files=(
  "AGENTS.md"
  "README.md"
  "CONTRIBUTING.md"
  "CHANGELOG.md"
  "LICENSE"
  ".editorconfig"
  ".gitignore"
  "docs/ARCHITECTURE.md"
  "docs/DEVELOPMENT.md"
  "docs/OPERATIONS.md"
  "docs/SECURITY.md"
  "docs/HANDOFF.md"
  "docs/PRODUCT.md"
  "docs/PROPOSALS.md"
  "docs/CONSTRAINTS.md"
  "docs/REQUIREMENTS.md"
  "tasks/CURRENT.md"
  "tasks/BACKLOG.md"
  "scripts/verify/verify.sh"
  ".github/pull_request_template.md"
)

for f in "${required_files[@]}"; do
  if [[ -s "${f}" ]]; then
    echo "PASS structure: ${f} exists and is non-empty"
  else
    echo "FAIL structure: ${f} is missing or empty"
    failures=$((failures + 1))
  fi
done

# CI workflow: active, or explicitly staged as pending (bootstrap, task T-008).
# Automation tokens cannot create files under .github/workflows/ (GitHub requires
# the `workflows` permission), so the staged state is only accepted while the
# activation task T-008 is open in tasks/BACKLOG.md.
if [[ -s ".github/workflows/ci.yml" ]]; then
  echo "PASS structure: .github/workflows/ci.yml exists and is non-empty"
elif [[ -s ".github/pending/ci.yml" ]] && grep -q "T-008" tasks/BACKLOG.md; then
  echo "PASS structure: CI workflow staged as pending (.github/pending/ci.yml, T-008) — activation required"
  echo "NOTE structure: pending state accepted only while T-008 is open; activation = move the file to .github/workflows/ci.yml via the GitHub web UI"
else
  echo "FAIL structure: no CI workflow (neither active .github/workflows/ci.yml nor staged .github/pending/ci.yml with open T-008)"
  failures=$((failures + 1))
fi

# At least one issue template must exist.
set -- .github/ISSUE_TEMPLATE/*.md
if [[ -e "${1}" ]]; then
  echo "PASS structure: .github/ISSUE_TEMPLATE/ contains at least one template"
else
  echo "FAIL structure: .github/ISSUE_TEMPLATE/ contains no templates"
  failures=$((failures + 1))
fi

# The entry point must be runnable directly and by CI.
if [[ -x "scripts/verify/verify.sh" ]]; then
  echo "PASS structure: scripts/verify/verify.sh is executable"
else
  echo "FAIL structure: scripts/verify/verify.sh is not executable"
  failures=$((failures + 1))
fi

if [[ "${failures}" -gt 0 ]]; then
  exit 1
fi
exit 0
