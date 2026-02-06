"""Unit tests for app.prompts."""

from __future__ import annotations

from app.models import SearchHit
from app.prompts import build_synthesis_prompt


def test_build_synthesis_prompt_contains_job_description():
    """Returned string contains job_description, company, role, tech list."""
    prompt = build_synthesis_prompt(
        job_description="Senior Engineer at Acme. Python, React.",
        company="Acme",
        role="Senior Engineer",
        technologies=["Python", "React"],
        company_results=[],
        tech_results={},
    )
    assert "Senior Engineer at Acme. Python, React." in prompt
    assert "Acme" in prompt
    assert "Senior Engineer" in prompt
    assert "Python" in prompt
    assert "React" in prompt


def test_build_synthesis_prompt_contains_company_research_section():
    """When company_results given, prompt contains 'Company Research' section."""
    hit = SearchHit(title="Acme Blog", url="https://acme.com/blog", snippets=["Snippet"])
    prompt = build_synthesis_prompt(
        job_description="Job",
        company="Acme",
        role="Engineer",
        technologies=[],
        company_results=[hit],
        tech_results={},
    )
    assert "Company Research" in prompt
    assert "Acme Blog" in prompt
    assert "https://acme.com/blog" in prompt


def test_build_synthesis_prompt_contains_tech_research_sections():
    """When tech_results given, prompt contains tech-named sections."""
    hit = SearchHit(title="Python Guide", url="https://py.org", snippets=["Tip"])
    prompt = build_synthesis_prompt(
        job_description="Job",
        company="Acme",
        role="Engineer",
        technologies=["Python"],
        company_results=[],
        tech_results={"Python": [hit]},
    )
    assert "Python Research" in prompt
    assert "Python Guide" in prompt


def test_build_synthesis_prompt_contains_schema_and_requirements():
    """Prompt contains schema snippet and 'Requirements'."""
    prompt = build_synthesis_prompt(
        job_description="Job",
        company="Acme",
        role="Engineer",
        technologies=[],
        company_results=[],
        tech_results={},
    )
    assert "companyName" in prompt
    assert "Requirements" in prompt
    assert "Easy" in prompt or "Medium" in prompt or "Hard" in prompt
