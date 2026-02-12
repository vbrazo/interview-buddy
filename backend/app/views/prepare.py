"""Prepare view — streaming response for /prepare."""

from __future__ import annotations

from fastapi.responses import StreamingResponse

from app.services.pipeline import run


def prepare_stream_response(job_description: str) -> StreamingResponse:
    """Build the SSE streaming response for the prepare endpoint."""
    return StreamingResponse(
        run(job_description),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
