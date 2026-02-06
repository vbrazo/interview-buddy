"""API route handlers."""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models import PrepareRequest
from app.pipeline import run

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
