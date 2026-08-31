#!/usr/bin/env bash
#
# verify_records.sh — append-only record integrity (AGENTS.md §4 rule 9).
#
# Guards against insertion-replacement loss in governing records:
#   - docs/PROPOSALS.md: P-entries unique and ascending; each entry keeps
#     its Source and Status lines; subsection counts match registered
#     anchors (exact, for known entries) or a floor of 3 (new entries).
#   - docs/HANDOFF.md: every record under "## Latest handoff records"
#     carries all required template fields (the template itself is not a record).
#
# When appending a new P-entry: register its subsection count in ANCHORS
# below (part of the append procedure, docs/DEVELOPMENT.md).

set -uo pipefail

failures=0

note_fail() {
  echo "FAIL records: ${1}"
  failures=$((failures + 1))
}

# 1. PROPOSALS: P-entries exist, are unique, and ascend in order.
nums="$(grep -oE '^## P-[0-9]+' docs/PROPOSALS.md | grep -oE '[0-9]+' || true)"
if [[ -z "${nums}" ]]; then
  note_fail "docs/PROPOSALS.md contains no '## P-<n>' entries"
else
  dupes="$(printf '%s\n' "${nums}" | sort | uniq -d || true)"
  asc="$(printf '%s\n' "${nums}" | awk 'NR>1 && $1<=prev {print} {prev=$1}')"
  if [[ -z "${dupes}" && -z "${asc}" ]]; then
    echo "PASS records: PROPOSALS P-entries are unique and ascending"
  else
    [[ -n "${dupes}" ]] && note_fail "duplicate P-entries: $(echo "${dupes}" | tr '\n' ' ')"
    [[ -n "${asc}" ]] && note_fail "P-entries out of ascending order at: $(echo "${asc}" | tr '\n' ' ')"
  fi
fi

# 2. PROPOSALS: every P-entry keeps Source + Status lines.
bad_entries="$(awk '
  /^## P-/ { if (id != "") { if (!src || !st) print id }
             id = $2; src = 0; st = 0; next }
  id != "" { if (/\*\*Source:\*\*/) src = 1
             if (/\*\*Status:\*\*/) st = 1 }
  END      { if (id != "" && (!src || !st)) print id }
' docs/PROPOSALS.md)"
if [[ -z "${bad_entries}" ]]; then
  echo "PASS records: every P-entry has Source/Status lines"
else
  note_fail "P-entries missing Source/Status: $(echo "${bad_entries}" | tr '\n' ' ')"
fi

# 3. PROPOSALS: subsection counts match anchors (exact) or floor (>= 3).
declare -A ANCHORS=( [1]=5 [2]=7 [3]=5 )
declare -A COUNT=()
cur=""
while IFS= read -r line; do
  case "${line}" in
    "## P-"[0-9]*)
      num="${line#\#\# P-}"
      num="${num%%[!0-9]*}"
      cur="${num}"
      COUNT["${cur}"]=0
      ;;
    "### "*)
      if [[ -n "${cur}" ]]; then
        COUNT["${cur}"]=$(( COUNT["${cur}"] + 1 ))
      fi
      ;;
  esac
done < docs/PROPOSALS.md
sub_ok=1
for k in "${!COUNT[@]}"; do
  if [[ -n "${ANCHORS[${k}]:-}" ]]; then
    if [[ "${COUNT[${k}]}" -ne "${ANCHORS[${k}]}" ]]; then
      note_fail "P-${k} has ${COUNT[${k}]} subsections, anchor expects ${ANCHORS[${k}]} — possible content loss"
      sub_ok=0
    fi
  elif [[ "${COUNT[${k}]}" -lt 3 ]]; then
    note_fail "P-${k} has ${COUNT[${k}]} subsections (below floor 3)"
    sub_ok=0
  fi
done
if [[ "${sub_ok}" -eq 1 ]]; then
  echo "PASS records: subsection counts match anchors/floor for all P-entries"
fi

# 4. HANDOFF: every record under '## Latest handoff records' is complete.
bad_records="$(awk '
  /^## Latest handoff records/ { started = 1 }
  started && /^### .*handoff/ { if (id != "") { if (!a || !b || !c || !d || !e || !f || !g) print id }
                                id = $0; a=b=c=d=e=f=g=0; next }
  id != "" { if (/Agent:/) a=1
             if (/Branch:/) b=1
             if (/Base commit:/) c=1
             if (/Head commit:/) d=1
             if (/Done \(state \+ evidence\):/) e=1
             if (/Not done/) f=1
             if (/Immediate next step:/) g=1 }
  END      { if (id != "" && (!a || !b || !c || !d || !e || !f || !g)) print id }
' docs/HANDOFF.md)"
if [[ -z "${bad_records}" ]]; then
  echo "PASS records: every handoff record carries all required fields"
else
  note_fail "incomplete handoff record(s): $(echo "${bad_records}" | tr '\n' ' ')"
fi

if [[ "${failures}" -gt 0 ]]; then
  exit 1
fi
exit 0
