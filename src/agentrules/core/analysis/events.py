"""Lightweight event primitives emitted during multi-phase analysis."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class AnalysisEvent:
    """Structured message describing a milestone in the analysis pipeline."""

    phase: str
    type: str
    payload: Mapping[str, Any]


class AnalysisEventSink(Protocol):
    """Simple interface for consumers interested in analysis events."""

    def publish(self, event: AnalysisEvent) -> None: ...


class NullEventSink:
    """No-op sink used when event handling is optional."""

    def publish(self, event: AnalysisEvent) -> None:  # pragma: no cover - intentional no-op
        return


__all__ = ["AnalysisEvent", "AnalysisEventSink", "NullEventSink"]
