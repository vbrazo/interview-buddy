"""Extract structured metadata from a job description string.

Renamed from ``parser.py`` to avoid shadowing the stdlib ``parser`` module.
"""

from __future__ import annotations

import re

from app.models import JobMetadata

# Sorted by category for readability; order doesn't affect matching.
_KNOWN_TECHNOLOGIES: tuple[str, ...] = (
    # Languages
    "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Golang",
    "Rust", "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R", "Dart", "Elixir",
    "Clojure", "Haskell", "Perl",
    # Frontend
    "React", "Angular", "Vue", "Vue.js", "Svelte", "Next.js", "Nuxt",
    "Gatsby", "Remix", "Astro", "Ember",
    # Backend
    "Node.js", "Express", "Django", "Flask", "FastAPI", "Spring",
    "Spring Boot", ".NET", "ASP.NET", "Rails", "Ruby on Rails", "Laravel",
    "Phoenix",
    # Databases
    "PostgreSQL", "Postgres", "MySQL", "MongoDB", "Redis", "Elasticsearch",
    "Cassandra", "DynamoDB", "SQLite", "SQL Server", "MariaDB",
    "Neo4j", "CockroachDB", "Supabase", "Firebase",
    # Cloud & Infra
    "AWS", "Azure", "GCP", "Google Cloud", "Docker", "Kubernetes",
    "Terraform", "Ansible", "Jenkins", "GitHub Actions", "GitLab CI",
    "Vercel", "Netlify",
    # Data & ML
    "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy", "Spark",
    "Hadoop", "Kafka", "Airflow", "dbt", "Snowflake", "BigQuery",
    "LangChain", "OpenAI",
    # Mobile
    "React Native", "Flutter", "SwiftUI",
    # Other
    "GraphQL", "REST", "gRPC", "WebSocket", "RabbitMQ", "Celery",
    "Linux", "Nginx", "Prometheus", "Grafana", "Datadog", "Sentry",
    # Concepts
    "distributed systems", "microservices", "CI/CD", "machine learning",
    "deep learning", "NLP", "computer vision", "data engineering",
    "DevOps", "SRE",
)

# Pre-compiled regex patterns for each technology (case-insensitive).
_TECH_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (tech, re.compile(r"\b" + re.escape(tech) + r"\b", re.IGNORECASE))
    for tech in _KNOWN_TECHNOLOGIES
]

# Patterns tried in order to extract the company name.
_COMPANY_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"(?:at|@)\s+([A-Z][A-Za-z0-9.\-]+)"),
    re.compile(r"(?:join|about)\s+([A-Z][A-Za-z0-9.\-]+)"),
    re.compile(r"([A-Z][A-Za-z0-9.\-]+)\s+is\s+(?:looking|hiring|seeking|building)"),
]


def extract_metadata(job_description: str) -> JobMetadata:
    """Return a ``JobMetadata`` from free-form *job_description* text."""
    return JobMetadata(
        company_name=_extract_company(job_description),
        role_title=_extract_role(job_description),
        technologies=_extract_technologies(job_description),
    )


# ── Private helpers ──────────────────────────────────────────────────

def _extract_company(text: str) -> str:
    for pattern in _COMPANY_PATTERNS:
        match = pattern.search(text)
        if match:
            name = match.group(1).strip().rstrip(".,;:!")
            if len(name) > 1:
                return name

    # Fallback: first line often contains "Role at Company"
    first_line = text.strip().split("\n")[0]
    at_match = re.search(r"at\s+(\S+)", first_line, re.IGNORECASE)
    if at_match:
        return at_match.group(1).strip().rstrip(".,;:!")

    return "the company"


def _extract_role(text: str) -> str:
    first_line = text.strip().split("\n")[0].strip()

    # "Senior Software Engineer at Company"
    match = re.match(r"^(.+?)\s+at\s+", first_line, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # "Title - Company" or "Title | Company"
    match = re.match(r"^(.+?)\s*[-|]\s*", first_line)
    if match:
        return match.group(1).strip()

    if len(first_line) < 80:
        return first_line

    return "Software Engineer"


def _extract_technologies(text: str, limit: int = 10) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []

    for tech, pattern in _TECH_PATTERNS:
        if pattern.search(text):
            key = tech.lower()
            if key not in seen:
                seen.add(key)
                unique.append(tech)

    return unique[:limit]
