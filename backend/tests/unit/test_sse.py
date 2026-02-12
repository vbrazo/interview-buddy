"""Unit tests for app.helpers.sse."""

from __future__ import annotations

import json

import pytest

from app.helpers.sse import (
    PIPELINE_STEPS,
    error_event,
    event,
    progress_event,
    result_event,
    steps_event,
)


def test_event_format():
    """event() returns 'data: <json>\\n\\n' with valid JSON."""
    data = {"type": "test", "value": 1}
    out = event(data)
    assert out.startswith("data: ")
    assert out.endswith("\n\n")
    payload = out[6:-2]
    parsed = json.loads(payload)
    assert parsed == data


def test_steps_event():
    """steps_event() has type 'steps' and steps list with emoji/text."""
    out = steps_event()
    assert "data: " in out
    payload = json.loads(out.split("data: ", 1)[1].strip())
    assert payload["type"] == "steps"
    assert "steps" in payload
    steps = payload["steps"]
    assert len(steps) == len(PIPELINE_STEPS)
    for s in steps:
        assert "emoji" in s
        assert "text" in s


def test_progress_event():
    """progress_event() has type 'progress', stepIndex, status in active/done, progress 0-99."""
    for step_index in (0, 2, 4):
        for status in ("active", "done"):
            out = progress_event(step_index, status)
            payload = json.loads(out.split("data: ", 1)[1].strip())
            assert payload["type"] == "progress"
            assert payload["stepIndex"] == step_index
            assert payload["status"] == status
            assert 0 <= payload["progress"] <= 99


def test_result_event():
    """result_event() has type 'result' and data present."""
    data = {"companyName": "Acme", "x": 1}
    out = result_event(data)
    payload = json.loads(out.split("data: ", 1)[1].strip())
    assert payload["type"] == "result"
    assert payload["data"] == data


def test_error_event():
    """error_event() has type 'error' and message present."""
    msg = "Something went wrong"
    out = error_event(msg)
    payload = json.loads(out.split("data: ", 1)[1].strip())
    assert payload["type"] == "error"
    assert payload["message"] == msg
