"""Prepare (interview analysis) controller."""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models import PrepareRequest
from app.views.prepare import prepare_stream_response

router = APIRouter(tags=["prepare"])


@router.post("/prepare")
async def prepare_interview(req: PrepareRequest) -> StreamingResponse:
    """Analyse a job description and stream the results via SSE."""
    return prepare_stream_response(req.jobDescription)
