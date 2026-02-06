"""API route handlers."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.models import PrepareRequest, SaveHistoryRequest
from app.services.history_store import delete as history_delete, get_by_id, list_all, save as history_save
from app.services.pipeline import run

router = APIRouter(prefix="/api")


@router.post("/prepare")
async def prepare_interview(req: PrepareRequest) -> StreamingResponse:
    """Analyse a job description and stream the results via SSE."""
    return StreamingResponse(
        run(req.jobDescription),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/health")
async def health() -> dict[str, str]:
    """Simple liveness check."""
    return {"status": "ok"}


# ── History (saved analyses) ─────────────────────────────────────────

@router.get("/history")
async def list_history() -> list:
    """List all saved analyses, newest first."""
    return [item.model_dump() for item in list_all()]


@router.post("/history")
async def save_to_history(req: SaveHistoryRequest) -> dict:
    """Save an analysis to history. Returns the created saved analysis."""
    entry = history_save(req.jobDescription, req.results)
    return entry.model_dump()


@router.get("/history/{id}")
async def get_history_item(id: str) -> dict:
    """Get one saved analysis by id."""
    entry = get_by_id(id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Not found")
    return entry.model_dump()


@router.delete("/history/{id}")
async def delete_history_item(id: str) -> dict[str, str]:
    """Delete a saved analysis."""
    if not history_delete(id):
        raise HTTPException(status_code=404, detail="Not found")
    return {"status": "ok"}
