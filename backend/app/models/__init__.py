"""Pydantic models shared across the backend. Re-export all for backward compatibility."""

from __future__ import annotations

from app.models.analysis import (
    AnalysisResult,
    Citation,
    CompanyInsight,
    InterviewFocus,
    PracticeQuestion,
    Resource,
    SavedAnalysis,
    SaveHistoryRequest,
    TechAnalysis,
    TechPoint,
)
from app.models.job_metadata import JobMetadata
from app.models.requests import PrepareRequest
from app.models.search import SearchHit

__all__ = [
    "AnalysisResult",
    "Citation",
    "CompanyInsight",
    "InterviewFocus",
    "JobMetadata",
    "PracticeQuestion",
    "PrepareRequest",
    "Resource",
    "SavedAnalysis",
    "SaveHistoryRequest",
    "SearchHit",
    "TechAnalysis",
    "TechPoint",
]
