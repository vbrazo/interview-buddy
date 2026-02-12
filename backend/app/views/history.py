"""History views — response shapes for history endpoints."""

from __future__ import annotations

from app.models import SavedAnalysis


def history_list_view(items: list[SavedAnalysis]) -> list[dict]:
    """Shape a list of saved analyses for the API response."""
    return [item.model_dump() for item in items]


def history_item_view(entry: SavedAnalysis) -> dict:
    """Shape a single saved analysis for the API response."""
    return entry.model_dump()


def history_delete_response() -> dict[str, str]:
    """Response body for successful history item deletion."""
    return {"status": "ok"}
