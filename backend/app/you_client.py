"""You.com API client — Search API (v1) and Research API (legacy).

Designed to be used as a managed singleton: call ``startup()`` once at app
boot to create the shared ``httpx.AsyncClient``, and ``shutdown()`` on
teardown.  The pipeline imports the module-level ``client`` instance.
"""

from __future__ import annotations

import logging
import uuid
from urllib.parse import urlparse

import httpx

from app.config import settings
from app.models import SearchHit
from app.prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)

# Module-level singleton.  Initialised in ``startup()``.
_http: httpx.AsyncClient | None = None


async def startup() -> None:
    """Create the shared ``httpx.AsyncClient``.  Call once at app boot."""
    global _http  # noqa: PLW0603
    settings.validate()
    _http = httpx.AsyncClient(timeout=max(settings.search_timeout, settings.chat_timeout))
    logger.info("YouClient HTTP pool initialised")


async def shutdown() -> None:
    """Close the shared client.  Call once at app shutdown."""
    global _http  # noqa: PLW0603
    if _http:
        await _http.aclose()
        _http = None
        logger.info("YouClient HTTP pool closed")


def _client() -> httpx.AsyncClient:
    if _http is None:
        raise RuntimeError("YouClient not initialised — call startup() first")
    return _http


# ── Search API (YDC v1) ──────────────────────────────────────────────

async def search(query: str, num_results: int | None = None) -> list[SearchHit]:
    """Search via You.com Search API v1 and return normalised ``SearchHit``s."""
    limit = num_results or settings.max_search_results
    resp = await _client().get(
        settings.you_search_url,
        params={"query": query, "count": limit},
        headers={"X-API-Key": settings.you_api_key},
        timeout=settings.search_timeout,
    )
    resp.raise_for_status()
    data = resp.json()

    hits: list[SearchHit] = []
    results = data.get("results") or {}
    for raw in results.get("web") or []:
        url = raw.get("url", "")
        snippets = raw.get("snippets") or []
        if isinstance(snippets, str):
            snippets = [snippets] if snippets else []
        hits.append(
            SearchHit(
                title=raw.get("title", ""),
                url=url,
                domain=urlparse(url).netloc if url else "",
                snippets=snippets,
            )
        )
    return hits


# ── Research API (legacy) ────────────────────────────────────────────

async def research(prompt: str) -> str:
    """Call You.com Research API and return the answer text."""
    query = f"{SYSTEM_PROMPT}\n\n---\n\n{prompt}"
    resp = await _client().post(
        settings.you_research_url,
        headers={
            "X-API-Key": settings.you_api_key,
            "Content-Type": "application/json",
        },
        json={
            "query": query,
            "chat_id": str(uuid.uuid4()),
        },
        timeout=settings.chat_timeout,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("answer", "")
