"""Job metadata extracted from a job description."""

from __future__ import annotations

from pydantic import BaseModel


class JobMetadata(BaseModel):
    company_name: str
    role_title: str
    technologies: list[str]
