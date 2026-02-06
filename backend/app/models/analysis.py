"""Analysis result and history models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Citation(BaseModel):
    title: str
    domain: str
    url: str


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


class SavedAnalysis(BaseModel):
    id: str
    jobDescription: str
    companyName: str
    roleTitle: str
    results: AnalysisResult
    savedAt: int  # Unix timestamp (ms)


class SaveHistoryRequest(BaseModel):
    jobDescription: str = Field(..., min_length=1)
    results: AnalysisResult
