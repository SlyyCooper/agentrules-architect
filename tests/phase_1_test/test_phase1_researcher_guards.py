"""Unit tests for Phase 1 researcher guardrails."""

from __future__ import annotations

import json
import unittest
from collections.abc import Sequence
from typing import Any
from unittest.mock import patch

from core.analysis.phase_1 import Phase1Analysis


class _StaticAgent:
    def __init__(self, name: str) -> None:
        self.name = name

    async def analyze(self, context: dict[str, Any], tools: Sequence[Any] | None = None) -> dict[str, Any]:
        return {"agent": self.name, "findings": {}}


class _NoToolResearcher:
    async def analyze(self, context: dict[str, Any], tools: Sequence[Any] | None = None) -> dict[str, Any]:
        return {"agent": "Researcher Agent", "findings": "fallback summary"}


class _FailingToolResearcher:
    def __init__(self) -> None:
        self.invocations = 0

    async def analyze(self, context: dict[str, Any], tools: Sequence[Any] | None = None) -> dict[str, Any]:
        self.invocations += 1
        if "tool_feedback" in context:
            return {"agent": "Researcher Agent", "findings": "tool feedback ignored"}
        return {
            "agent": "Researcher Agent",
            "findings": None,
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "tavily_web_search",
                        "arguments": json.dumps({
                            "query": "flask",
                            "search_depth": "basic",
                            "max_results": 1,
                        })
                    },
                }
            ],
        }


def _stub_architect_factory(phase: str, **kwargs: Any) -> _StaticAgent:  # pragma: no cover - helper
    name = kwargs.get("name") or f"{phase.title()} Agent"
    return _StaticAgent(name)


class Phase1ResearcherGuardrailsTests(unittest.IsolatedAsyncioTestCase):
    async def test_researcher_skipped_when_no_tools_requested(self) -> None:
        with patch("core.analysis.phase_1.get_architect_for_phase", side_effect=_stub_architect_factory), \
                patch("core.analysis.phase_1.get_researcher_architect", return_value=_NoToolResearcher()):
            analyzer = Phase1Analysis(researcher_enabled=True)
            result = await analyzer.run([], {})

        research_output = result["documentation_research"]
        self.assertEqual(research_output["status"], "skipped")
        self.assertEqual(research_output["reason"], "researcher-no-tools")

    async def test_researcher_skipped_when_all_tools_fail(self) -> None:
        async def failing_tavily(query: str, depth: str, max_results: int) -> str:  # pragma: no cover - injected
            return json.dumps({"error": "service unavailable"})

        with patch("core.analysis.phase_1.get_architect_for_phase", side_effect=_stub_architect_factory), \
                patch("core.analysis.phase_1.get_researcher_architect", return_value=_FailingToolResearcher()), \
                patch("core.analysis.phase_1._run_tavily_search", side_effect=failing_tavily):
            analyzer = Phase1Analysis(researcher_enabled=True)
            result = await analyzer.run([], {})

        research_output = result["documentation_research"]
        self.assertEqual(research_output["status"], "skipped")
        self.assertEqual(research_output["reason"], "researcher-tools-failed")
        executed_tools = research_output.get("executed_tools", [])
        self.assertTrue(executed_tools)
        self.assertTrue(all("error" in record for record in executed_tools))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
