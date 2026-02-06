"""Pydantic models shared across the backend."""

from __future__ import annotations

from pydantic import BaseModel, Field


# ── Request ──────────────────────────────────────────────────────────
class PrepareRequest(BaseModel):
    jobDescription: str = Field(..., min_length=1)


# ── Job metadata extracted from the description ─────────────────────
class JobMetadata(BaseModel):
    company_name: str
    role_title: str
    technologies: list[str]


# ── Search result (normalised from You.com response) ────────────────
class SearchHit(BaseModel):
    title: str = ""
    url: str = ""
    domain: str = ""
    snippets: list[str] = Field(default_factory=list)


# ── Citation attached to insights / tech points ─────────────────────
class Citation(BaseModel):
    title: str
    domain: str
    url: str


# ── Sections of the final analysis result ───────────────────────────
class CompanyInsight(BaseModel):
    text: str
    citation: Citation | None = None


class TechPoint(BaseModel):
    text: str
    citation: Citation | None = None


class TechAnalysis(BaseModel):
    name: str
    points: list[TechPoint]


class InterviewFocus(BaseModel):
    topic: str
    difficulty: str  # "Easy" | "Medium" | "Hard"
    description: str


class PracticeQuestion(BaseModel):
    question: str
    difficulty: str
    category: str
    hint: str


class Resource(BaseModel):
    title: str
    domain: str
    url: str
    description: str


class AnalysisResult(BaseModel):
    companyName: str
    companyIntelligence: list[CompanyInsight]
    techAnalysis: list[TechAnalysis]
    interviewFocus: list[InterviewFocus]
    practiceQuestions: list[PracticeQuestion]
    resources: list[Resource]
