"""Helpers for preparing OpenAI API request payloads."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from agentrules.core.agents.base import ReasoningMode

ApiType = Literal["responses", "chat"]


@dataclass(frozen=True)
class PreparedRequest:
    """Represents a fully constructed request ready for dispatch."""

    api: ApiType
    payload: dict[str, Any]


def prepare_request(
    *,
    model_name: str,
    content: str,
    reasoning: ReasoningMode,
    temperature: float | None,
    tools: list[Any] | None,
    text_verbosity: str | None,
    use_responses_api: bool,
) -> PreparedRequest:
    """Build an OpenAI SDK request payload based on the active model pathway."""
    if use_responses_api:
        payload: dict[str, Any] = {
            "model": model_name,
            "input": content,
        }

        reasoning_payload = _build_responses_reasoning_payload(reasoning)
        if reasoning_payload:
            payload["reasoning"] = reasoning_payload

        text_config = _build_text_config(text_verbosity)
        if text_config:
            payload["text"] = text_config

        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        return PreparedRequest(api="responses", payload=payload)

    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": content,
            }
        ],
    }

    reasoning_params = _build_chat_reasoning_params(model_name, reasoning)
    if reasoning_params:
        payload.update(reasoning_params)

    if _should_attach_temperature(model_name, reasoning, temperature):
        payload["temperature"] = temperature

    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"

    return PreparedRequest(api="chat", payload=payload)


def _build_responses_reasoning_payload(reasoning: ReasoningMode) -> dict[str, str] | None:
    if reasoning in {
        ReasoningMode.MINIMAL,
        ReasoningMode.LOW,
        ReasoningMode.MEDIUM,
        ReasoningMode.HIGH,
    }:
        return {"effort": reasoning.value}

    if reasoning == ReasoningMode.ENABLED:
        return {"effort": ReasoningMode.MEDIUM.value}

    return None


def _build_text_config(text_verbosity: str | None) -> dict[str, Any] | None:
    if not text_verbosity:
        return None
    return {"verbosity": text_verbosity}


def _build_chat_reasoning_params(
    model_name: str,
    reasoning: ReasoningMode,
) -> dict[str, Any] | None:
    normalized = model_name.lower()
    if normalized not in {"o3", "o4-mini"}:
        return None

    if reasoning == ReasoningMode.ENABLED:
        effort = "high"
    elif reasoning == ReasoningMode.MINIMAL:
        effort = ReasoningMode.LOW.value
    elif reasoning in {ReasoningMode.LOW, ReasoningMode.MEDIUM, ReasoningMode.HIGH}:
        effort = reasoning.value
    else:
        effort = ReasoningMode.MEDIUM.value

    return {"reasoning_effort": effort}


def _should_attach_temperature(
    model_name: str,
    reasoning: ReasoningMode,
    temperature: float | None,
) -> bool:
    if temperature is None:
        return False

    return reasoning == ReasoningMode.TEMPERATURE or model_name.lower() == "gpt-4.1"
