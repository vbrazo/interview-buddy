"""Request body models for API routes."""

from __future__ import annotations

from pydantic import BaseModel, Field


class PrepareRequest(BaseModel):
    jobDescription: str = Field(..., min_length=1)
