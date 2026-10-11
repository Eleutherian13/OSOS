"""Watch target categories explicitly.
Unknown categories are rejected rather than silently accepted."""
from __future__ import annotations

CATEGORIES = {
    "GSoC_TIMELINE",
    "GSoC_RULES",
    "GSoC_AI_GUIDANCE",
    "LFX_DOCS",
    "ORG_CONTRIBUTING",
    "ORG_AI_POLICY",
    "ORG_PROJECT_IDEAS",
    "ORG_CONTACT",
}


def validate_category(value: str) -> str:
    if value not in CATEGORIES:
        raise ValueError(f"unknown watch category: {value!r}")
    return value
