"""Unit tests for app.config."""

from __future__ import annotations

import pytest


def test_settings_validate_raises_when_api_key_empty():
    """settings.validate() raises ValueError when YOU_API_KEY is empty."""
    from app.config import Settings

    settings = Settings(you_api_key="")
    with pytest.raises(ValueError, match="YOU_API_KEY"):
        settings.validate()


def test_settings_validate_does_not_raise_when_api_key_set():
    """settings.validate() does not raise when YOU_API_KEY is non-empty."""
    from app.config import Settings

    settings = Settings(you_api_key="test-key")
    settings.validate()
