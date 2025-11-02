
import pytest

from agentrules.core.agents.anthropic import AnthropicArchitect
from agentrules.core.agents.anthropic import client as anthropic_client


class _BlockText:
    def __init__(self, text):
        self.text = text


class _ToolUse:
    def __init__(self, id, name, input):
        self.id = id
        self.name = name
        self.input = input


class _BlockTool:
    def __init__(self, id, name, input):
        self.tool_use = _ToolUse(id, name, input)


class _FakeResponse:
    def __init__(self, content):
        self.content = content


class _FakeMessages:
    def __init__(self, resp):
        self._resp = resp

    def create(self, **kwargs):
        return self._resp


class _FakeClient:
    def __init__(self, resp):
        self.messages = _FakeMessages(resp)


@pytest.mark.asyncio
async def test_anthropic_analyze_parses_text_and_tools(monkeypatch):
    # Create a fake response containing both text and tool_use
    resp = _FakeResponse([
        _BlockTool("id1", "tavily_web_search", {"query": "x"}),
        _BlockText("analysis text"),
    ])
    anthropic_client.set_client(_FakeClient(resp))
    try:
        arch = AnthropicArchitect()
        out = await arch.analyze({"formatted_prompt": "ctx"})
        assert out["findings"] == "analysis text"
        assert isinstance(out["tool_calls"], list)
        assert out["tool_calls"][0]["name"] == "tavily_web_search"
    finally:
        anthropic_client.set_client(None)


@pytest.mark.asyncio
async def test_anthropic_analyze_parses_dict_tool_use(monkeypatch):
    resp = _FakeResponse([
        {"type": "thinking", "thinking": "inspecting"},
        {
            "type": "tool_use",
            "id": "toolu_123",
            "name": "tavily_web_search",
            "input": {"query": "framework"},
        },
        {"type": "text", "text": "final analysis"},
    ])
    anthropic_client.set_client(_FakeClient(resp))
    try:
        arch = AnthropicArchitect()
        out = await arch.analyze({"formatted_prompt": "ctx"})
        assert out["findings"] == "final analysis"
        assert out["tool_calls"] == [
            {
                "id": "toolu_123",
                "name": "tavily_web_search",
                "input": {"query": "framework"},
            }
        ]
    finally:
        anthropic_client.set_client(None)
