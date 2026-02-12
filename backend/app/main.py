"""Interview Buddy — FastAPI application factory."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.controllers import router
from app.services import you_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Path to frontend build directory (relative to backend/)
FRONTEND_DIST = Path(__file__).parent.parent.parent / "dist"


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage startup / shutdown of shared resources."""
    await you_client.startup()
    logger.info("Application started")
    yield
    await you_client.shutdown()
    logger.info("Application shut down")


def create_app() -> FastAPI:
    """Build and return the configured FastAPI application."""
    app = FastAPI(title="Interview Buddy API", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # API routes
    app.include_router(router)

    # Serve static files from frontend build (if dist/ exists)
    if FRONTEND_DIST.exists() and (FRONTEND_DIST / "index.html").exists():
        # Mount static assets directory if it exists (Vite outputs to dist/assets/)
        assets_dir = FRONTEND_DIST / "assets"
        if assets_dir.exists():
            app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")
        
        # Serve other static files and handle SPA routing
        @app.get("/{path:path}")
        async def serve_spa(request: Request, path: str):
            """Serve the React app for all non-API routes (SPA routing)."""
            # Don't serve API routes as static files
            if path.startswith("api/"):
                return {"error": "Not found"}
            
            # Don't serve assets (already mounted above)
            if path.startswith("assets/"):
                return {"error": "Not found"}
            
            # Check if it's a static file request (favicon, robots.txt, etc.)
            file_path = FRONTEND_DIST / path
            if file_path.exists() and file_path.is_file():
                return FileResponse(str(file_path))
            
            # For all other routes, serve index.html (SPA routing)
            index_path = FRONTEND_DIST / "index.html"
            if index_path.exists():
                return FileResponse(str(index_path))
            
            return {"error": "Frontend not built"}
        
        logger.info(f"Serving frontend from {FRONTEND_DIST}")
    else:
        logger.warning(f"Frontend dist not found at {FRONTEND_DIST}, serving API only")

    return app


app = create_app()
