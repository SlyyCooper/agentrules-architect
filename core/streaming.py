"""Common streaming event types shared across provider implementations."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Union


class StreamEventType(str, Enum):
    """Normalized event types emitted by provider streaming implementations."""

    TEXT_DELTA = "text_delta"
    REASONING_DELTA = "reasoning_delta"
    TOOL_CALL_DELTA = "tool_call_delta"
    MESSAGE_START = "message_start"
    MESSAGE_DELTA = "message_delta"
    MESSAGE_END = "message_end"
    USAGE = "usage"
    ERROR = "error"
    SYSTEM = "system"


JsonMapping = Union[Mapping[str, Any], MutableMapping[str, Any]]


@dataclass
class StreamChunk:
    """Normalized representation of a streaming payload chunk."""

    event_type: StreamEventType
    text: Optional[str] = None
    reasoning: Optional[str] = None
    tool_call: Optional[JsonMapping] = None
    finish_reason: Optional[str] = None
    usage: Optional[JsonMapping] = None
    raw: Optional[Any] = None
