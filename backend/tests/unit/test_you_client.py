"""Unit tests for app.you_client (with mocked HTTP)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.models import SearchHit
from app.services import you_client


@pytest.fixture
def mock_http():
    """Provide a mock AsyncClient for you_client._http."""
    client = MagicMock()
    client.get = AsyncMock()
    client.post = AsyncMock()
    return client


@pytest.mark.asyncio
async def test_search_parses_v1_response(mock_http):
    """search() parses v1 response (results.web) into list of SearchHit."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "results": {
            "web": [
                {
                    "url": "https://example.com/page",
                    "title": "Example Page",
                    "snippets": ["Snippet one", "Snippet two"],
                },
            ],
        },
    }
    mock_resp.raise_for_status = MagicMock()
    mock_http.get.return_value = mock_resp

    with patch.object(you_client, "_http", mock_http):
        hits = await you_client.search("test query", num_results=5)

    assert len(hits) == 1
    assert hits[0].title == "Example Page"
    assert hits[0].url == "https://example.com/page"
    assert hits[0].domain == "example.com"
    assert hits[0].snippets == ["Snippet one", "Snippet two"]


@pytest.mark.asyncio
async def test_search_parses_legacy_response(mock_http):
    """search() parses legacy response (hits) when v1 returns 403 and legacy is used."""
    # First call (v1) returns 403; second call (legacy) returns 200 with hits.
    # Config already has you_search_legacy_url, so no need to patch frozen settings.
    legacy_resp = MagicMock()
    legacy_resp.status_code = 200
    legacy_resp.json.return_value = {
        "hits": [
            {
                "url": "https://legacy.com/doc",
                "title": "Legacy Doc",
                "description": "Fallback description",
            },
        ],
    }
    legacy_resp.raise_for_status = MagicMock()

    v1_resp = MagicMock()
    v1_resp.status_code = 403

    mock_http.get.side_effect = [v1_resp, legacy_resp]

    with patch.object(you_client, "_http", mock_http):
        hits = await you_client.search("query")

    assert len(hits) == 1
    assert hits[0].title == "Legacy Doc"
    assert hits[0].url == "https://legacy.com/doc"
    assert hits[0].domain == "legacy.com"
    assert hits[0].snippets == ["Fallback description"]


@pytest.mark.asyncio
async def test_research_returns_message_answer_text(mock_http):
    """research() returns text from output item with type message.answer."""
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "output": [
            {"type": "other", "content": []},
            {"type": "message.answer", "text": "  {\"companyName\": \"Acme\"}  "},
        ],
    }
    mock_resp.raise_for_status = MagicMock()
    mock_http.post.return_value = mock_resp

    with patch.object(you_client, "_http", mock_http):
        out = await you_client.research("Some prompt")

    assert out == "{\"companyName\": \"Acme\"}"


@pytest.mark.asyncio
async def test_research_returns_empty_when_no_answer(mock_http):
    """research() returns empty string when no message.answer in output."""
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"output": [{"type": "web_search.results", "content": []}]}
    mock_resp.raise_for_status = MagicMock()
    mock_http.post.return_value = mock_resp

    with patch.object(you_client, "_http", mock_http):
        out = await you_client.research("prompt")

    assert out == ""
