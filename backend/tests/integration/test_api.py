"""Integration tests for API routes."""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models import AnalysisResult
from app.repositories.history_store import clear_store


@pytest.fixture(autouse=True)
def _clear_history():
    clear_store()
    yield
    clear_store()


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

    with patch("app.services.pipeline.you_client.search", side_effect=mock_search):
        with patch("app.services.pipeline.you_client.research", side_effect=mock_research):
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


# ── History API ──────────────────────────────────────────────────────

def _minimal_analysis_result(company: str = "Acme") -> dict:
    return {
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


def test_history_list_empty():
    """GET /api/history returns 200 and empty list when no items."""
    client = TestClient(app)
    resp = client.get("/api/history")
    assert resp.status_code == 200
    assert resp.json() == []


def test_history_save_and_list():
    """POST /api/history creates item; GET /api/history returns it."""
    client = TestClient(app)
    body = {
        "jobDescription": "Senior Engineer at Acme. Python, React.",
        "results": _minimal_analysis_result("Acme"),
    }
    resp = client.post("/api/history", json=body)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"]
    assert data["companyName"] == "Acme"
    assert data["jobDescription"] == body["jobDescription"]
    assert data["savedAt"] > 0

    resp2 = client.get("/api/history")
    assert resp2.status_code == 200
    items = resp2.json()
    assert len(items) == 1
    assert items[0]["id"] == data["id"]


def test_history_get_by_id():
    """GET /api/history/{id} returns the item; 404 if not found."""
    client = TestClient(app)
    body = {
        "jobDescription": "Job at Beta.",
        "results": _minimal_analysis_result("Beta"),
    }
    create = client.post("/api/history", json=body)
    assert create.status_code == 200
    id = create.json()["id"]

    resp = client.get(f"/api/history/{id}")
    assert resp.status_code == 200
    assert resp.json()["companyName"] == "Beta"

    resp404 = client.get("/api/history/nonexistent-id")
    assert resp404.status_code == 404


def test_history_delete():
    """DELETE /api/history/{id} removes the item; 404 if not found."""
    client = TestClient(app)
    body = {
        "jobDescription": "Job at Gamma.",
        "results": _minimal_analysis_result("Gamma"),
    }
    create = client.post("/api/history", json=body)
    id = create.json()["id"]

    resp = client.delete(f"/api/history/{id}")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

    assert client.get(f"/api/history/{id}").status_code == 404
    assert client.delete(f"/api/history/{id}").status_code == 404


def test_history_save_invalid_body_returns_422():
    """POST /api/history with missing jobDescription or results returns 422."""
    client = TestClient(app)
    results = _minimal_analysis_result()
    assert client.post("/api/history", json={}).status_code == 422
    assert client.post("/api/history", json={"jobDescription": "x"}).status_code == 422
    assert client.post("/api/history", json={"results": results}).status_code == 422
