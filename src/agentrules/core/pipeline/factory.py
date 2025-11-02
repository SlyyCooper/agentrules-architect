"""Factory helpers for constructing analysis pipelines."""

from __future__ import annotations

from agentrules.core.analysis import (
    FinalAnalysis,
    Phase1Analysis,
    Phase2Analysis,
    Phase3Analysis,
    Phase4Analysis,
    Phase5Analysis,
)
from agentrules.core.analysis.events import AnalysisEventSink

from .orchestrator import AnalysisPipeline


def create_default_pipeline(
    *,
    researcher_enabled: bool,
    event_sink: AnalysisEventSink | None = None,
) -> AnalysisPipeline:
    """Build an `AnalysisPipeline` with the standard phase implementations."""

    return AnalysisPipeline(
        phase1=Phase1Analysis(researcher_enabled=researcher_enabled),
        phase2=Phase2Analysis(),
        phase3=Phase3Analysis(),
        phase4=Phase4Analysis(),
        phase5=Phase5Analysis(),
        final=FinalAnalysis(),
        event_sink=event_sink,
    )
