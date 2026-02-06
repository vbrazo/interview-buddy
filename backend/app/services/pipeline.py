"""Analysis pipeline — orchestrates parsing, search, and synthesis.

Yields SSE-formatted strings so that the route handler can stream them
directly via ``StreamingResponse``.
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import AsyncGenerator

from app.config import settings
from app.models import AnalysisResult, SearchHit
from app.services import you_client
from app.services.job_parser import extract_metadata
from app.services.prompts import build_synthesis_prompt
from app.services.sse import (
    error_event,
    progress_event,
    result_event,
    steps_event,
)

logger = logging.getLogger(__name__)


async def run(job_description: str) -> AsyncGenerator[str, None]:
    """Execute the full interview-prep pipeline, yielding SSE events."""

    # ── Step definitions ─────────────────────────────────────────────
    yield steps_event()

    # ── Step 0: extract metadata ─────────────────────────────────────
    yield progress_event(0, "active")
    metadata = extract_metadata(job_description)
    logger.info(
        "Extracted: company=%s  role=%s  techs=%s",
        metadata.company_name,
        metadata.role_title,
        metadata.technologies,
    )
    await asyncio.sleep(0.3)  # brief UX pause
    yield progress_event(0, "done")

    # ── Step 1: company research (Search API) ────────────────────────
    yield progress_event(1, "active")
    company_hits = await _search_company(metadata.company_name)
    yield progress_event(1, "done")

    # ── Step 2: tech-stack research (Search API) ─────────────────────
    yield progress_event(2, "active")
    tech_hits = await _search_technologies(metadata.technologies)
    yield progress_event(2, "done")

    # ── Step 3: synthesis (Chat completions) ─────────────────────────
    yield progress_event(3, "active")

    prompt = build_synthesis_prompt(
        job_description=job_description,
        company=metadata.company_name,
        role=metadata.role_title,
        technologies=metadata.technologies,
        company_results=company_hits,
        tech_results=tech_hits,
    )

    try:
        analysis = await _synthesise(prompt, metadata.company_name)
    except (json.JSONDecodeError, ValueError) as exc:
        logger.error("Synthesis parse error: %s", exc)
        yield error_event("Failed to parse AI response. Please try again.")
        return
    except Exception as exc:
        logger.error("Synthesis failed: %s", exc)
        yield error_event(f"Analysis failed: {exc}")
        return

    yield progress_event(3, "done")

    # ── Step 4: done ─────────────────────────────────────────────────
    yield progress_event(4, "active")
    await asyncio.sleep(0.2)
    yield progress_event(4, "done")

    yield result_event(analysis.model_dump())


# ── Private helpers ──────────────────────────────────────────────────

async def _search_company(company: str) -> list[SearchHit]:
    """Run a single company-focused search query."""
    try:
        hits = await you_client.search(
            f"{company} company recent news product launches 2025 2026"
        )
        logger.info("Company search returned %d results", len(hits))
        return hits
    except Exception as exc:
        logger.warning("Company search failed: %s", exc)
        return []


async def _search_technologies(
    technologies: list[str],
) -> dict[str, list[SearchHit]]:
    """Run one search query per technology (capped by config)."""
    results: dict[str, list[SearchHit]] = {}
    for tech in technologies[: settings.max_technologies]:
        try:
            hits = await you_client.search(
                f"{tech} best practices interview questions 2025"
            )
            results[tech] = hits
        except Exception as exc:
            logger.warning("Tech search for %s failed: %s", tech, exc)
    logger.info("Tech search completed for %d technologies", len(results))
    return results


async def _synthesise(prompt: str, fallback_company: str) -> AnalysisResult:
    """Call the research-mode LLM and parse its output into an ``AnalysisResult``."""
    raw = await you_client.research(prompt)
    content = _strip_markdown_fences(raw)
    data: dict = json.loads(content)

    # Guarantee the company name is present
    if not data.get("companyName"):
        data["companyName"] = fallback_company

    return AnalysisResult.model_validate(data)


def _strip_markdown_fences(text: str) -> str:
    """Remove accidental ```json ... ``` wrapping from LLM output."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()
