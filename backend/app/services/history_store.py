"""In-memory store for saved analyses (history). Replace with DB/Redis for persistence."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import AnalysisResult, SavedAnalysis

_store: dict[str, SavedAnalysis] = {}


def list_all() -> list[SavedAnalysis]:
    """Return all saved analyses, newest first."""
    from app.models import SavedAnalysis

    items = list(_store.values())
    items.sort(key=lambda x: x.savedAt, reverse=True)
    return items


def get_by_id(id: str) -> SavedAnalysis | None:
    """Return one saved analysis by id."""
    return _store.get(id)


def save(job_description: str, results: AnalysisResult) -> SavedAnalysis:
    """Create and store a saved analysis. Returns the created SavedAnalysis."""
    from app.models import SavedAnalysis

    entry = SavedAnalysis(
        id=str(uuid.uuid4()),
        jobDescription=job_description,
        companyName=results.companyName,
        roleTitle=f"{results.companyName} Analysis",
        results=results,
        savedAt=_timestamp_ms(),
    )
    _store[entry.id] = entry
    return entry


def delete(id: str) -> bool:
    """Remove a saved analysis. Returns True if it existed."""
    if id in _store:
        del _store[id]
        return True
    return False


def clear_all() -> None:
    """Remove all entries. For testing only."""
    _store.clear()


def _timestamp_ms() -> int:
    import time
    return int(time.time() * 1000)


def clear_store() -> None:
    """Clear all entries. For testing only."""
    _store.clear()
