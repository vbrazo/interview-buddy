"""History (saved analyses) controller."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.models import SaveHistoryRequest
from app.repositories.history_store import delete as history_delete, get_by_id, list_all, save as history_save
from app.views.history import (
    history_delete_response,
    history_item_view,
    history_list_view,
)

router = APIRouter(tags=["history"])


@router.get("/history")
async def list_history() -> list:
    """List all saved analyses, newest first."""
    return history_list_view(list_all())


@router.post("/history")
async def save_to_history(req: SaveHistoryRequest) -> dict:
    """Save an analysis to history. Returns the created saved analysis."""
    entry = history_save(req.jobDescription, req.results)
    return history_item_view(entry)


@router.get("/history/{id}")
async def get_history_item(id: str) -> dict:
    """Get one saved analysis by id."""
    entry = get_by_id(id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Not found")
    return history_item_view(entry)


@router.delete("/history/{id}")
async def delete_history_item(id: str) -> dict[str, str]:
    """Delete a saved analysis."""
    if not history_delete(id):
        raise HTTPException(status_code=404, detail="Not found")
    return history_delete_response()
