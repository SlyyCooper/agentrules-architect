"""Helpers for constructing Anthropic Messages API payloads."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from agentrules.core.agents.base import ReasoningMode

DEFAULT_MAX_TOKENS = 20_000
DEFAULT_THINKING_BUDGET = 16_000


@dataclass(frozen=True)
class PreparedRequest:
    """Container for a ready-to-dispatch Anthropic request."""

    payload: dict[str, Any]


def prepare_request(
    *,
    model_name: str,
    prompt: str,
    reasoning: ReasoningMode,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    tools: list[Any] | None,
) -> PreparedRequest:
    payload: dict[str, Any] = {
        "model": model_name,
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }

    thinking = _build_thinking_payload(reasoning)
    if thinking is not None:
        payload["thinking"] = thinking

    if tools:
        payload["tools"] = tools

    return PreparedRequest(payload=payload)


def _build_thinking_payload(reasoning: ReasoningMode) -> dict[str, Any] | None:
    if reasoning == ReasoningMode.ENABLED:
        return {"type": "enabled", "budget_tokens": DEFAULT_THINKING_BUDGET}

    if reasoning == ReasoningMode.DYNAMIC:
        # Dynamic mode allows the caller to opt-in to Anthropic's adaptive thinking.
        return {"type": "dynamic"}

    if reasoning == ReasoningMode.DISABLED:
        return None

    return None
