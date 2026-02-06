"""Centralised application settings loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True, slots=True)
class Settings:
    """Immutable application settings."""

    you_api_key: str = os.getenv("YOU_API_KEY", "")

    # You.com API endpoints (see docs.you.com/api-reference)
    # Search v1: GET .../v1/search (X-API-Key, query, count)
    you_search_url: str = os.getenv("YOU_SEARCH_URL", "https://ydc-index.io/v1/search")
    # Search legacy fallback if v1 returns 403
    you_search_legacy_url: str = "https://api.ydc-index.io/search"
    # Express Agent for synthesis: POST .../v1/agents/runs (Bearer token, agent, input)
    you_agents_runs_url: str = os.getenv(
        "YOU_AGENTS_RUNS_URL", "https://api.you.com/v1/agents/runs"
    )

    # Defaults
    search_timeout: float = 30.0
    chat_timeout: float = 120.0
    max_search_results: int = 5
    max_technologies: int = 5

    def validate(self) -> None:
        """Raise if required settings are missing."""
        if not self.you_api_key:
            raise ValueError(
                "YOU_API_KEY is not set. "
                "Copy .env.example to .env and add your key."
            )


settings = Settings()
