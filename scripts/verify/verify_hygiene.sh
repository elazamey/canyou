#!/usr/bin/env bash
#
# verify_hygiene.sh — generic hygiene over governance files.
#
# No conflict markers, no placeholder content, no trailing whitespace,
# and every governance file ends with a newline.

set -uo pipefail

failures=0

governance_paths=(
  "AGENTS.md"
  "README.md"
  "CONTRIBUTING.md"
  "CHANGELOG.md"
  "docs"
  "tasks"
  "scripts"
  ".github"
)

# 1. No unresolved merge-conflict markers in tracked files.
conflicts="$(git grep -n -I -E '^(<{7} |={7}$|>{7} )' -- . || true)"
if [[ -z "${conflicts}" ]]; then
  echo "PASS hygiene: no merge-conflict markers in tracked files"
else
  echo "FAIL hygiene: merge-conflict markers found:"
  printf '%s\n' "${conflicts}" | sed 's/^/    /'
  failures=$((failures + 1))
fi

# 2. No placeholder/filler tokens in documentation files.
#    Matches filler tokens (template variables, lorem ipsum), not the English
#    word "placeholder" in prose. scripts/ is excluded: check scripts must be
#    allowed to mention the patterns they enforce.
placeholders="$(grep -rn -I -i -E 'LOREM IPSUM|_PLACEHOLDER|PLACEHOLDER_|<PLACEHOLDER>' \
  AGENTS.md README.md CONTRIBUTING.md CHANGELOG.md LICENSE docs tasks 2>/dev/null || true)"
if [[ -z "${placeholders}" ]]; then
  echo "PASS hygiene: no placeholder/filler tokens in documentation"
else
  echo "FAIL hygiene: placeholder/filler tokens found:"
  printf '%s\n' "${placeholders}" | sed 's/^/    /'
  failures=$((failures + 1))
fi

# 3. No trailing whitespace in governance text files.
trailing="$(grep -rn -I -E '[[:space:]]+$' \
  --include='*.md' --include='*.yml' --include='*.yaml' --include='*.sh' \
  "${governance_paths[@]}" 2>/dev/null || true)"
if [[ -z "${trailing}" ]]; then
  echo "PASS hygiene: no trailing whitespace in governance files"
else
  echo "FAIL hygiene: trailing whitespace found:"
  printf '%s\n' "${trailing}" | sed 's/^/    /'
  failures=$((failures + 1))
fi

# 4. Governance text files end with a newline.
nonewline=0
for f in \
  *.md scripts/verify/*.sh docs/*.md tasks/*.md \
  .github/workflows/*.yml .github/pending/*.yml .github/ISSUE_TEMPLATE/*.md .github/*.md; do
  [[ -e "${f}" ]] || continue
  last_byte="$(tail -c 1 "${f}")"
  if [[ -n "${last_byte}" ]]; then
    echo "FAIL hygiene: ${f} does not end with a newline"
    nonewline=1
    failures=$((failures + 1))
  fi
done
if [[ "${nonewline}" -eq 0 ]]; then
  echo "PASS hygiene: all governance files end with a newline"
fi

if [[ "${failures}" -gt 0 ]]; then
  exit 1
fi
exit 0
