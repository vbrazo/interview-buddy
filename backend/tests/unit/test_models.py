"""Unit tests for app.models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.models import (
    AnalysisResult,
    JobMetadata,
    PrepareRequest,
    SearchHit,
)


def test_prepare_request_valid():
    """PrepareRequest accepts non-empty jobDescription."""
    req = PrepareRequest(jobDescription="Senior Engineer at Acme. Python.")
    assert req.jobDescription == "Senior Engineer at Acme. Python."


def test_prepare_request_empty_raises():
    """PrepareRequest with empty jobDescription raises ValidationError."""
    with pytest.raises(ValidationError):
        PrepareRequest(jobDescription="")


def test_job_metadata_required_fields():
    """JobMetadata requires company_name, role_title, technologies."""
    m = JobMetadata(
        company_name="Acme",
        role_title="Engineer",
        technologies=["Python"],
    )
    assert m.company_name == "Acme"
    assert m.role_title == "Engineer"
    assert m.technologies == ["Python"]


def test_search_hit_defaults():
    """SearchHit has defaults for title, url, domain, snippets."""
    hit = SearchHit()
    assert hit.title == ""
    assert hit.url == ""
    assert hit.domain == ""
    assert hit.snippets == []


def test_search_hit_with_values():
    """SearchHit accepts title, url, domain, snippets."""
    hit = SearchHit(
        title="A Page",
        url="https://example.com/page",
        domain="example.com",
        snippets=["snippet one"],
    )
    assert hit.title == "A Page"
    assert hit.url == "https://example.com/page"
    assert hit.domain == "example.com"
    assert hit.snippets == ["snippet one"]


def _valid_analysis_dict():
    """Minimal valid dict for AnalysisResult."""
    return {
        "companyName": "Acme",
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


def test_analysis_result_valid():
    """AnalysisResult accepts valid dict with all required sections."""
    data = _valid_analysis_dict()
    result = AnalysisResult.model_validate(data)
    assert result.companyName == "Acme"
    assert len(result.companyIntelligence) == 1
    assert len(result.techAnalysis) == 1
    assert len(result.interviewFocus) == 1
    assert len(result.practiceQuestions) == 1
    assert len(result.resources) == 1


def test_analysis_result_missing_company_raises():
    """AnalysisResult with missing companyName raises ValidationError."""
    data = _valid_analysis_dict()
    del data["companyName"]
    with pytest.raises(ValidationError):
        AnalysisResult.model_validate(data)


def test_analysis_result_missing_company_intelligence_raises():
    """AnalysisResult with missing companyIntelligence raises ValidationError."""
    data = _valid_analysis_dict()
    del data["companyIntelligence"]
    with pytest.raises(ValidationError):
        AnalysisResult.model_validate(data)
