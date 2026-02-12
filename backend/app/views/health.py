"""Health check view — response shape for /health."""

from __future__ import annotations


def health_response() -> dict[str, str]:
    """Return the health check response body."""
    return {"status": "ok"}
