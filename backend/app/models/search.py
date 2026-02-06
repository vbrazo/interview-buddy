"""Search result (normalised from You.com response)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class SearchHit(BaseModel):
    title: str = ""
    url: str = ""
    domain: str = ""
    snippets: list[str] = Field(default_factory=list)
