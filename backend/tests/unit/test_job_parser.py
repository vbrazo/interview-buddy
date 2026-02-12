"""Unit tests for app.helpers.job_parser."""

from __future__ import annotations

import pytest

from app.helpers.job_parser import extract_metadata


def test_extract_company_at_pattern():
    """Company extracted from 'Title at Company'."""
    text = "Senior Software Engineer at Acme\nWe use Python and React."
    m = extract_metadata(text)
    assert m.company_name == "Acme"


def test_extract_company_join_pattern():
    """Company extracted from 'join Company' (pattern is case-sensitive)."""
    text = "join Stripe and build payments. Python, Go."
    m = extract_metadata(text)
    assert m.company_name == "Stripe"


def test_extract_company_is_hiring_pattern():
    """Company extracted from 'Company is hiring'."""
    text = "Acme is hiring a Backend Engineer. Django, PostgreSQL."
    m = extract_metadata(text)
    assert m.company_name == "Acme"


def test_extract_company_fallback_first_line():
    """Company fallback from first line 'at Company'."""
    text = "Engineer at ExampleCo\n\nLong description here."
    m = extract_metadata(text)
    assert m.company_name == "ExampleCo"


def test_extract_company_default():
    """Company defaults to 'the company' when nothing matches."""
    text = "Some role\nNo company name here. Just a long paragraph."
    m = extract_metadata(text)
    assert m.company_name == "the company"


def test_extract_role_title_at_company():
    """Role extracted from 'Title at Company'."""
    text = "Senior Software Engineer at Acme\nPython."
    m = extract_metadata(text)
    assert m.role_title == "Senior Software Engineer"


def test_extract_role_title_dash_company():
    """Role extracted from 'Title - Company'."""
    text = "Backend Engineer - Acme Inc\nWe use Go."
    m = extract_metadata(text)
    assert m.role_title == "Backend Engineer"


def test_extract_role_short_first_line():
    """Role is first line when under 80 chars and no at/dash."""
    text = "Software Engineer\nAt Acme we do Python."
    m = extract_metadata(text)
    assert m.role_title == "Software Engineer"


def test_extract_role_default_long_first_line():
    """Role defaults to Software Engineer when first line very long."""
    text = "A" * 100 + "\nAt Acme. Python."
    m = extract_metadata(text)
    assert m.role_title == "Software Engineer"


def test_extract_technologies_known_techs():
    """Known technologies detected case-insensitively."""
    text = "Engineer at Acme. We use python, REACT, and aws."
    m = extract_metadata(text)
    assert "Python" in m.technologies
    assert "React" in m.technologies
    assert "AWS" in m.technologies


def test_extract_technologies_deduplicated():
    """Technologies are deduplicated (e.g. Python once)."""
    text = "Engineer at Acme. Python and Python. python again."
    m = extract_metadata(text)
    assert m.technologies.count("Python") == 1
    assert "Python" in m.technologies


def test_extract_technologies_capped():
    """Technologies list is capped (e.g. 10)."""
    text = (
        "Engineer at Acme. Python JavaScript TypeScript Java C++ C# Go Rust Ruby PHP "
        "Swift Kotlin Scala React Angular Vue Django Flask"
    )
    m = extract_metadata(text)
    assert len(m.technologies) <= 10


def test_extract_metadata_empty_string():
    """Empty string gives default company, empty role, no techs."""
    m = extract_metadata("")
    assert m.company_name == "the company"
    assert m.role_title == ""
    assert m.technologies == []
