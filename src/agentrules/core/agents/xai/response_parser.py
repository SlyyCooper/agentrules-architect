"""Utilities for normalising xAI chat completion responses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ParsedResponse:
    """Canonical representation of an xAI response."""

    findings: str | None
    tool_calls: list[dict[str, Any]] | None
    reasoning: str | None
    encrypted_reasoning: str | None


def parse_response(response: Any) -> ParsedResponse:
    """Extract findings and tool call metadata from the SDK response."""
    message = response.choices[0].message
    findings = getattr(message, "content", None) or None
    tool_calls = _normalise_tool_calls(getattr(message, "tool_calls", None))
    reasoning = _normalise_reasoning(getattr(message, "reasoning_content", None))
    encrypted_reasoning = _normalise_reasoning(getattr(message, "encrypted_content", None))

    return ParsedResponse(
        findings=findings,
        tool_calls=tool_calls,
        reasoning=reasoning,
        encrypted_reasoning=encrypted_reasoning,
    )


def _normalise_tool_calls(tool_calls: Any) -> list[dict[str, Any]] | None:
    if not tool_calls:
        return None

    normalised: list[dict[str, Any]] = []
    for call in tool_calls:
        call_type = _extract(call, "type")
        if call_type != "function":
            continue
        function = _extract(call, "function") or {}
        normalised.append(
            {
                "id": _extract(call, "id"),
                "type": call_type,
                "function": {
                    "name": _extract(function, "name"),
                    "arguments": _extract(function, "arguments"),
                },
            }
        )
    return normalised or None


def _extract(obj: Any, attr: str) -> Any:
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj.get(attr)
    return getattr(obj, attr, None)


def _normalise_reasoning(raw: Any) -> str | None:
    if raw is None:
        return None
    if isinstance(raw, str):
        return raw
    if isinstance(raw, list):
        parts: list[str] = []
        for item in raw:
            if isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
                else:
                    parts.append(str(item))
            else:
                parts.append(str(item))
        return "\n".join(parts).strip() or None
    return str(raw)
