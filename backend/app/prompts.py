"""Prompt templates for the You.com chat completions call."""

from __future__ import annotations

from app.models import SearchHit

# ── System prompt ────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "You are an expert interview preparation assistant. "
    "You research companies and technologies to help candidates "
    "prepare for job interviews. Always respond with valid JSON "
    "only — no markdown fences, no commentary outside the JSON."
)

# ── JSON schema example shown to the model ───────────────────────────
_SCHEMA_EXAMPLE = """\
{{
  "companyName": "{company}",
  "companyIntelligence": [
    {{
      "text": "Insight about the company...",
      "citation": {{"title": "Source Title", "domain": "example.com", "url": "https://example.com/article"}}
    }}
  ],
  "techAnalysis": [
    {{
      "name": "TechnologyName",
      "points": [
        {{
          "text": "Key point about this technology...",
          "citation": {{"title": "Source", "domain": "example.com", "url": "https://example.com"}}
        }}
      ]
    }}
  ],
  "interviewFocus": [
    {{
      "topic": "Topic Name",
      "difficulty": "Easy|Medium|Hard",
      "description": "What to prepare for..."
    }}
  ],
  "practiceQuestions": [
    {{
      "question": "Interview question...",
      "difficulty": "Easy|Medium|Hard",
      "category": "Category",
      "hint": "Guidance for answering..."
    }}
  ],
  "resources": [
    {{
      "title": "Resource Name",
      "domain": "example.com",
      "url": "https://example.com",
      "description": "Why this resource is useful..."
    }}
  ]
}}"""

# ── Requirements appended after the schema ───────────────────────────
_REQUIREMENTS = """\
Requirements:
- Include 4-6 company intelligence items with citations where possible
- Include analysis for each key technology mentioned ({tech_list})
- Include 5-7 interview focus areas with varied difficulty levels
- Include 8-10 practice questions spanning technical and behavioral
- Include 4-6 useful resources relevant to the role
- Use REAL URLs from the research results above when available
- difficulty must be exactly one of: "Easy", "Medium", "Hard"
- All citations should reference actual sources"""


# ── Public builder ───────────────────────────────────────────────────
def build_synthesis_prompt(
    job_description: str,
    company: str,
    role: str,
    technologies: list[str],
    company_results: list[SearchHit],
    tech_results: dict[str, list[SearchHit]],
) -> str:
    """Assemble the full user prompt for the synthesis step."""
    tech_list = ", ".join(technologies) if technologies else "general software engineering"

    company_context = _format_search_context("Company Research", company_results)
    tech_context = "".join(
        _format_search_context(f"{tech} Research", hits)
        for tech, hits in tech_results.items()
    )

    schema = _SCHEMA_EXAMPLE.format(company=company)
    requirements = _REQUIREMENTS.format(tech_list=tech_list)

    return f"""\
Based on this job description and my research, create a comprehensive interview preparation guide.

JOB DESCRIPTION:
{job_description}

EXTRACTED INFO:
- Company: {company}
- Role: {role}
- Key Technologies: {tech_list}

{company_context}
{tech_context}

Respond with a JSON object matching this EXACT schema (no markdown fences, just raw JSON):
{schema}

{requirements}"""


def _format_search_context(title: str, hits: list[SearchHit]) -> str:
    """Render search hits as a markdown-style context block for the prompt."""
    if not hits:
        return ""
    lines = [f"\n{title}:"]
    for hit in hits[:5]:
        snippet_text = " ".join(hit.snippets[:2])[:300]
        lines.append(f"- [{hit.title}]({hit.url}) — {snippet_text}")
    return "\n".join(lines) + "\n"
