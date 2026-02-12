"""Helpers for formatting Server-Sent Events."""

from __future__ import annotations

import json
from typing import Any

# Step definitions displayed in the frontend streaming UI.
PIPELINE_STEPS: list[dict[str, str]] = [
    {"emoji": "⏳", "text": "Extracting job details..."},
    {"emoji": "🔍", "text": "Researching company..."},
    {"emoji": "📊", "text": "Analyzing tech stack..."},
    {"emoji": "🧠", "text": "Synthesizing interview prep..."},
    {"emoji": "✅", "text": "Complete!"},
]


def event(data: dict[str, Any]) -> str:
    """Serialise *data* as a single SSE ``data:`` line."""
    return f"data: {json.dumps(data)}\n\n"


def steps_event() -> str:
    """Return the initial SSE event that defines the pipeline steps."""
    return event({"type": "steps", "steps": PIPELINE_STEPS})


def progress_event(step_index: int, status: str) -> str:
    """Return a progress SSE event.

    *status* is ``"active"`` or ``"done"``.
    Progress percentage is derived from the step index.
    """
    total = len(PIPELINE_STEPS)
    frac = (step_index + (1.0 if status == "done" else 0.5)) / total
    return event(
        {
            "type": "progress",
            "stepIndex": step_index,
            "status": status,
            "progress": min(int(frac * 100), 99),
        }
    )


def result_event(data: dict[str, Any]) -> str:
    """Return the final result SSE event."""
    return event({"type": "result", "data": data})


def error_event(message: str) -> str:
    """Return an error SSE event."""
    return event({"type": "error", "message": message})
