"""Integration tests for API routes."""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models import AnalysisResult


def _minimal_analysis_json(company: str = "Acme") -> str:
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


def test_health_returns_ok():
    """GET /api/health returns 200 and { status: ok }."""
    client = TestClient(app)
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_prepare_valid_body_streams_sse_with_steps_progress_result():
    """POST /api/prepare with valid body streams SSE: steps, progress, result."""
    async def mock_search(_query: str):
        return []

    async def mock_research(_prompt: str):
        return _minimal_analysis_json("Acme")

    with patch("app.pipeline.you_client.search", side_effect=mock_search):
        with patch("app.pipeline.you_client.research", side_effect=mock_research):
            client = TestClient(app)
            resp = client.post(
                "/api/prepare",
                json={"jobDescription": "Senior Engineer at Acme. Python, React."},
            )

    assert resp.status_code == 200
    assert "text/event-stream" in resp.headers.get("content-type", "")

    text = resp.text
    types = []
    for line in text.split("\n"):
        if line.startswith("data: "):
            try:
                payload = json.loads(line[6:].strip())
                types.append(payload.get("type"))
                if payload.get("type") == "result":
                    AnalysisResult.model_validate(payload["data"])
            except json.JSONDecodeError:
                pass

    assert "steps" in types
    assert "progress" in types
    assert "result" in types


def test_prepare_missing_job_description_returns_422():
    """POST /api/prepare with missing jobDescription returns 422."""
    client = TestClient(app)
    resp = client.post("/api/prepare", json={})
    assert resp.status_code == 422


def test_prepare_empty_job_description_returns_422():
    """POST /api/prepare with empty jobDescription returns 422."""
    client = TestClient(app)
    resp = client.post("/api/prepare", json={"jobDescription": ""})
    assert resp.status_code == 422
