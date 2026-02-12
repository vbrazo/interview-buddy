"""API routes — assembles controllers under /api."""

from __future__ import annotations

from fastapi import APIRouter

from app.controllers.health import router as health_router
from app.controllers.history import router as history_router
from app.controllers.prepare import router as prepare_router

router = APIRouter(prefix="/api")

router.include_router(health_router)
router.include_router(prepare_router)
router.include_router(history_router)
