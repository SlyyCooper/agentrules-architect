"""Prompt helpers for Anthropic architects."""
from __future__ import annotations

import json
from collections.abc import Iterable
from typing import Any


def default_prompt_template() -> str:
    """Return the default prompt template applied when none is provided."""
    return (
        "You are {agent_name}, responsible for {agent_role}.\n\n"
        "Your specific responsibilities are:\n"
        "{agent_responsibilities}\n\n"
        "Analyze this project context and provide a detailed report focused on your domain:\n\n"
        "{context}\n\n"
        "Format your response as a structured report with clear sections and findings."
    )


def _format_responsibilities(responsibilities: Iterable[str] | None) -> str:
    if not responsibilities:
        return "- (no specific responsibilities provided)"
    return "\n".join(f"- {item}" for item in responsibilities)


def format_prompt(
    *,
    template: str,
    agent_name: str,
    agent_role: str,
    responsibilities: Iterable[str] | None,
    context: dict[str, Any] | Any,
) -> str:
    """Fill the template with architect metadata and analysis context."""
    context_str = json.dumps(context, indent=2) if isinstance(context, dict) else str(context)
    return template.format(
        agent_name=agent_name,
        agent_role=agent_role,
        agent_responsibilities=_format_responsibilities(responsibilities),
        context=context_str,
    )
