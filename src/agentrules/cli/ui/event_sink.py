"""Event sink bridging analysis events with the Rich-based CLI view."""

from __future__ import annotations

from numbers import Real

from agentrules.core.analysis.events import AnalysisEvent, AnalysisEventSink

from .analysis_view import AnalysisView


class ViewEventSink(AnalysisEventSink):
    """Translate analysis events into Rich-rendered status updates."""

    PHASE_COLORS = {
        "phase2": "blue",
        "phase3": "yellow",
    }

    def __init__(self, view: AnalysisView):
        self.view = view
        self._agents: dict[str, dict] = {}

    def publish(self, event: AnalysisEvent) -> None:
        if event.phase == "phase2" and event.type == "agent_plan":
            agents = list(event.payload.get("agents", []))
            self._cache_agents(agents)
            self.view.render_agent_plan(agents, color=self.PHASE_COLORS["phase2"])
            return

        if event.phase not in self.PHASE_COLORS:
            return

        phase_color = self.PHASE_COLORS[event.phase]
        payload = dict(event.payload)
        agent_id = payload.get("id")
        if agent_id:
            agent_info = self._agents.setdefault(agent_id, {})
            agent_info.update(payload)
        agent_name = self._resolve_agent_name(payload)

        if event.type == "agent_registered":
            detail = self._format_file_detail(payload.get("files"))
            message = f"Pending{detail}" if detail else "Pending"
            self.view.update_agent_progress(
                event.phase,
                agent_id or agent_name,
                agent_name,
                message,
                "⏳",
                phase_color,
                phase_color,
            )
            return
        if event.type == "agent_started":
            detail = self._format_file_detail(payload.get("files"))
            message = f"In progress{detail}"
            self.view.update_agent_progress(
                event.phase,
                agent_id or agent_name,
                agent_name,
                message,
                "⟳",
                phase_color,
                phase_color,
            )
        elif event.type == "agent_completed":
            message = "Completed"
            duration = payload.get("duration")
            if isinstance(duration, Real):
                message += f" in {duration:.1f}s"
            self.view.update_agent_progress(
                event.phase,
                agent_id or agent_name,
                agent_name,
                message,
                "✓",
                phase_color,
                phase_color,
            )
        elif event.type == "agent_failed":
            error = payload.get("error", "unknown error")
            duration = payload.get("duration")
            message = f"Failed: {error}"
            if isinstance(duration, Real):
                message += f" after {duration:.1f}s"
            self.view.update_agent_progress(
                event.phase,
                agent_id or agent_name,
                agent_name,
                message,
                "✗",
                "red",
                phase_color,
            )

    def _cache_agents(self, agents: list[dict]) -> None:
        for entry in agents:
            agent_id = entry.get("id")
            if agent_id:
                self._agents.setdefault(agent_id, {}).update(entry)

    def _resolve_agent_name(self, payload: dict) -> str:
        if payload.get("name"):
            return str(payload["name"])
        if payload.get("id"):
            return str(payload["id"])
        return "Agent"

    def _format_file_detail(self, files: object) -> str:
        if not files:
            return ""
        try:
            count = len(files)  # type: ignore[arg-type]
        except TypeError:
            return ""
        label = "file" if count == 1 else "files"
        return f" · {count} {label}"
