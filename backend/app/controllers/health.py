"""Health check controller."""

from __future__ import annotations

from fastapi import APIRouter

from app.views.health import health_response

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, str]:
    """Simple liveness check."""
    return health_response()
