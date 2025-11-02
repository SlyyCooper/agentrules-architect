"""Anthropic SDK client helpers."""
from __future__ import annotations

from typing import Any

from anthropic import Anthropic

_client: Anthropic | Any | None = None


def get_client() -> Any:
    """Return a cached Anthropic SDK client instance."""
    global _client
    if _client is None:
        _client = Anthropic()
    return _client


def set_client(client: Any | None) -> None:
    """Override the cached client, primarily for tests."""
    global _client
    _client = client


def execute_message_request(payload: dict) -> Any:
    """Execute a Claude Messages API call with the provided payload."""
    client = get_client()
    return client.messages.create(**payload)
