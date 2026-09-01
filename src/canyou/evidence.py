"""Evidence — the minimal per-execution trace record (R-5, directive section 8).

Every invocation attempt emits one :class:`TraceRecord` carrying:
``execution_id``, ``agent_id``, ``tool_id``, ``timestamp``,
``policy_decision`` (plus a machine-readable reason), and *references* to
the input/output evidence — sha256 over the canonical payload. The payload
itself is never recorded, so a secret passed in arguments or results cannot
leak into evidence. This is the Gate's minimal auditable record (R-5) —
deliberately not an Execution Ledger component (R-7, owner decision Q-6).

:class:`EvidenceLog` is append-only through its public interface: records
enter via :meth:`EvidenceLog.append` and are readable as immutable
snapshots; no update or delete operation exists.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any, Iterator, List, Tuple


def reference_of(payload: Any) -> str:
    """Content reference: sha256 over the canonical JSON of ``payload``.

    Returns only the hash — never the payload — so no secret inside
    arguments or results can reach the evidence log.
    """
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class TraceRecord:
    """One gate decision record: R-5's four fields plus the section-8 superset."""

    execution_id: str
    agent_id: str
    tool_id: str
    timestamp: str
    policy_decision: str
    policy_reason: str
    input_reference: str
    output_reference: str
    artifact_reference: str | None = None


class EvidenceLog:
    """Append-only collection of trace records for one run."""

    def __init__(self) -> None:
        self._records: List[TraceRecord] = []

    def append(self, record: TraceRecord) -> None:
        """Append one record; the only mutating public method (R-5)."""
        if not isinstance(record, TraceRecord):
            raise TypeError("EvidenceLog accepts TraceRecord instances only")
        self._records.append(record)

    def records(self) -> Tuple[TraceRecord, ...]:
        """Immutable snapshot of all records, in append order (R-5)."""
        return tuple(self._records)

    def to_json_lines(self) -> str:
        """Serialize as JSON-lines with sorted keys (deterministic)."""
        return "\n".join(
            json.dumps(asdict(record), sort_keys=True) for record in self._records
        )

    def __iter__(self) -> Iterator[TraceRecord]:
        return iter(self.records())

    def __len__(self) -> int:
        return len(self._records)
