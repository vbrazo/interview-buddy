"""You.com API client — Search API and Research-mode chat completions.

Designed to be used as a managed singleton: call ``startup()`` once at app
boot to create the shared ``httpx.AsyncClient``, and ``shutdown()`` on
teardown.  The pipeline imports the module-level ``client`` instance.
"""

from __future__ import annotations

import logging
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


# ── Search API ───────────────────────────────────────────────────────

async def search(query: str, num_results: int | None = None) -> list[SearchHit]:
    """Search via You.com Search API and return normalised ``SearchHit``s."""
    limit = num_results or settings.max_search_results
    resp = await _client().get(
        settings.you_search_url,
        params={"query": query, "num_web_results": limit},
        headers={"X-API-Key": settings.you_api_key},
        timeout=settings.search_timeout,
    )
    resp.raise_for_status()
    data = resp.json()

    hits: list[SearchHit] = []
    for raw in data.get("hits", []):
        url = raw.get("url", "")
        hits.append(
            SearchHit(
                title=raw.get("title", ""),
                url=url,
                domain=urlparse(url).netloc if url else "",
                snippets=raw.get("snippets", []),
            )
        )
    return hits


# ── Chat completions (Research mode) ─────────────────────────────────

async def research(prompt: str) -> str:
    """Send a research-mode chat completion and return the assistant content."""
    resp = await _client().post(
        settings.you_chat_url,
        headers={
            "Authorization": f"Bearer {settings.you_api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": settings.you_chat_model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        },
        timeout=settings.chat_timeout,
    )
    resp.raise_for_status()
    data = resp.json()

    content: str = (
        data.get("choices", [{}])[0]
        .get("message", {})
        .get("content", "")
    )
    return content
