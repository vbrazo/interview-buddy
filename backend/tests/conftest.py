"""Shared pytest fixtures and environment for backend tests."""

from __future__ import annotations

import os

import pytest


@pytest.fixture(scope="session", autouse=True)
def set_test_env():
    """Ensure YOU_API_KEY is set so you_client.startup() does not fail in integration tests."""
    os.environ.setdefault("YOU_API_KEY", "test-key-for-pytest")
