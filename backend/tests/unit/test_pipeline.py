"""Unit tests for app.pipeline (with mocked you_client)."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, patch

import pytest

from app.models import AnalysisResult, SearchHit
from app.services.pipeline import run


def _minimal_analysis_json(company: str = "Acme") -> str:
    """Valid JSON string that parses to AnalysisResult."""
    data = {
        "companyName": company,
        "companyIntelligence": [
            {"text": "Insight", "citation": {"title": "T", "domain": "d", "url": "https://u"}},
        ],
        "techAnalysis": [
            {"name": "Python", "points": [{"text": "Point", "citation": None}]},
        ],
        "interviewFocus": [
            {"topic": "T", "difficulty": "Easy", "description": "D"},
        ],
        "practiceQuestions": [
            {"question": "Q?", "difficulty": "Medium", "category": "Tech", "hint": "H"},
        ],
        "resources": [
            {"title": "R", "domain": "d", "url": "https://u", "description": "D"},
        ],
    }
    return json.dumps(data)


@pytest.mark.asyncio
async def test_run_happy_path_yields_steps_progress_result():
    """run() yields steps, progress events, and result with valid AnalysisResult data."""
    search_hits: list[SearchHit] = [
        SearchHit(title="A", url="https://a.com", domain="a.com", snippets=["s"]),
    ]

    async def mock_search(_query: str):
        return search_hits

    async def mock_research(_prompt: str):
        return _minimal_analysis_json("Acme")

    events: list[str] = []
    with patch("app.services.pipeline.you_client.search", side_effect=mock_search):
        with patch("app.services.pipeline.you_client.research", side_effect=mock_research):
            async for chunk in run("Senior Engineer at Acme. Python, React."):
                events.append(chunk)

    types = []
    for ev in events:
        if not ev.startswith("data: "):
            continue
        payload = json.loads(ev[6:].strip())
        types.append(payload.get("type"))
        if payload.get("type") == "result":
            result = AnalysisResult.model_validate(payload["data"])
            assert result.companyName == "Acme"

    assert "steps" in types
    assert "progress" in types
    assert "result" in types
    assert types.count("steps") == 1
    assert types.count("result") == 1


@pytest.mark.asyncio
async def test_run_synthesis_error_yields_error_event():
    """When research returns invalid JSON, run() yields error event and no result."""
    async def mock_search(_query: str):
        return []

    async def mock_research(_prompt: str):
        return "not valid json {{{"

    events: list[str] = []
    with patch("app.services.pipeline.you_client.search", side_effect=mock_search):
        with patch("app.services.pipeline.you_client.research", side_effect=mock_research):
            async for chunk in run("Engineer at Acme."):
                events.append(chunk)

    types = []
    for ev in events:
        if not ev.startswith("data: "):
            continue
        payload = json.loads(ev[6:].strip())
        types.append(payload.get("type"))

    assert "error" in types
    assert "result" not in types


@pytest.mark.asyncio
async def test_run_synthesis_exception_yields_error_event():
    """When research raises, run() yields error event."""
    async def mock_search(_query: str):
        return []

    async def mock_research(_prompt: str):
        raise RuntimeError("API down")

    events: list[str] = []
    with patch("app.services.pipeline.you_client.search", side_effect=mock_search):
        with patch("app.services.pipeline.you_client.research", side_effect=mock_research):
            async for chunk in run("Engineer at Acme."):
                events.append(chunk)

    types = []
    for ev in events:
        if not ev.startswith("data: "):
            continue
        payload = json.loads(ev[6:].strip())
        types.append(payload.get("type"))

    assert "error" in types
    assert "result" not in types
