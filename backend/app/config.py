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

    # You.com API endpoints (current Search v1 + Research legacy)
    you_search_url: str = "https://ydc-index.io/v1/search"
    you_research_url: str = "https://chat-api.you.com/research"

    # Defaults
    you_chat_model: str = "gpt-4o-mini"
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
