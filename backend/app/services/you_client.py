"""You.com API client — Search (v1) and Express Agent for synthesis.

- Search: GET https://ydc-index.io/v1/search (X-API-Key, query, count)
- Synthesis: POST https://api.you.com/v1/agents/runs (Bearer, agent=express, input)

Designed to be used as a managed singleton: call ``startup()`` once at app
boot to create the shared ``httpx.AsyncClient``, and ``shutdown()`` on
teardown.
"""

from __future__ import annotations

import logging
from urllib.parse import urlparse

import httpx

from app.config import settings
from app.models import SearchHit
from app.services.prompts import SYSTEM_PROMPT

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
    """Search via You.com Search API; tries v1 first, then legacy if v1 returns 403."""
    limit = num_results or settings.max_search_results
    headers = {"X-API-Key": settings.you_api_key}

    # Try v1 endpoint first (GET .../v1/search, params: query, count)
    resp = await _client().get(
        settings.you_search_url,
        params={"query": query, "count": limit, "language": "EN"},
        headers=headers,
        timeout=settings.search_timeout,
    )

    if resp.status_code == 403 and getattr(settings, "you_search_legacy_url", None):
        # Fallback to legacy endpoint (GET .../search, params: query, num_web_results)
        logger.info("Search v1 returned 403, trying legacy endpoint")
        resp = await _client().get(
            settings.you_search_legacy_url,
            params={"query": query, "num_web_results": limit},
            headers=headers,
            timeout=settings.search_timeout,
        )

    resp.raise_for_status()
    data = resp.json()

    # v1 response: data.results.web[]
    results = data.get("results") or {}
    web = results.get("web")
    if web is not None:
        return _parse_web_hits(web)

    # Legacy response: data.hits[]
    legacy_hits = data.get("hits") or []
    return _parse_legacy_hits(legacy_hits)


def _parse_web_hits(raw_list: list) -> list[SearchHit]:
    hits: list[SearchHit] = []
    for raw in raw_list:
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


def _parse_legacy_hits(raw_list: list) -> list[SearchHit]:
    hits: list[SearchHit] = []
    for raw in raw_list:
        url = raw.get("url", "")
        snippets = raw.get("snippets") or []
        if isinstance(snippets, str):
            snippets = [snippets] if snippets else []
        desc = raw.get("description", "")
        if not snippets and desc:
            snippets = [desc]
        hits.append(
            SearchHit(
                title=raw.get("title", ""),
                url=url,
                domain=urlparse(url).netloc if url else "",
                snippets=snippets,
            )
        )
    return hits


# ── Express Agent — synthesis ──────────────────────────────────────────
# https://docs.you.com/api-reference/agents/express-agent/express-agent-runs

async def research(prompt: str) -> str:
    """Call You.com Express Agent and return the answer text (e.g. JSON string)."""
    instructions = (
        "Respond with valid JSON only. No markdown code fences, no commentary. "
        "Follow the exact schema requested in the user message."
    )
    input_text = f"{instructions}\n\n---\n\n{prompt}"
    resp = await _client().post(
        settings.you_agents_runs_url,
        headers={
            "Authorization": f"Bearer {settings.you_api_key}",
            "Content-Type": "application/json",
        },
        json={
            "agent": "express",
            "input": input_text,
            "stream": False,
        },
        timeout=settings.chat_timeout,
    )
    resp.raise_for_status()
    data = resp.json()
    for item in data.get("output") or []:
        if item.get("type") == "message.answer" and item.get("text"):
            return (item["text"] or "").strip()
    return ""
