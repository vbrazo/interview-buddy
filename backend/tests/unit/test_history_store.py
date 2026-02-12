"""Unit tests for app.repositories.history_store."""

from __future__ import annotations

import pytest

from app.models import AnalysisResult, SavedAnalysis
from app.repositories.history_store import clear_store, delete, get_by_id, list_all, save


def _minimal_result(company: str = "Acme") -> AnalysisResult:
    return AnalysisResult(
        companyName=company,
        companyIntelligence=[],
        techAnalysis=[],
        interviewFocus=[],
        practiceQuestions=[],
        resources=[],
    )


@pytest.fixture(autouse=True)
def _clear_before_each():
    clear_store()
    yield
    clear_store()


def test_save_returns_saved_analysis():
    """save() creates an entry and returns it with id and savedAt."""
    result = _minimal_result("Acme")
    entry = save("Job at Acme. Python.", result)
    assert isinstance(entry, SavedAnalysis)
    assert entry.id
    assert entry.companyName == "Acme"
    assert entry.jobDescription == "Job at Acme. Python."
    assert entry.savedAt > 0


def test_list_all_returns_newest_first():
    """list_all() returns entries sorted by savedAt descending."""
    import time
    save("First", _minimal_result("A"))
    time.sleep(0.01)
    save("Second", _minimal_result("B"))
    time.sleep(0.01)
    save("Third", _minimal_result("C"))
    items = list_all()
    assert len(items) == 3
    assert items[0].companyName == "C"
    assert items[1].companyName == "B"
    assert items[2].companyName == "A"


def test_get_by_id():
    """get_by_id() returns the entry or None."""
    entry = save("Job", _minimal_result("X"))
    assert get_by_id(entry.id) is not None
    assert get_by_id(entry.id).companyName == "X"
    assert get_by_id("nonexistent") is None


def test_delete():
    """delete() removes the entry and returns True; returns False if not found."""
    entry = save("Job", _minimal_result("Y"))
    assert get_by_id(entry.id) is not None
    assert delete(entry.id) is True
    assert get_by_id(entry.id) is None
    assert delete(entry.id) is False
    assert delete("nonexistent") is False
