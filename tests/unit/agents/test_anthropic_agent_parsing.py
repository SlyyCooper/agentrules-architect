import unittest

from agentrules.core.agents.anthropic import AnthropicArchitect
from agentrules.core.agents.anthropic import client as anthropic_client
from tests.fakes.vendor_responses import AnthropicMessageCreateResponseFake, _AnthropicToolUseBlock


class _AnthropicFakeMessagesAPI:
    def __init__(self):
        self.last_params = None

    def create(self, **params):
        self.last_params = params
        # Return a text block and a tool_use block
        tool_block = _AnthropicToolUseBlock("call_1", "web_search", {"query": "Flask docs"})
        return AnthropicMessageCreateResponseFake(text="analysis", tool_call=tool_block)


class _AnthropicFakeClient:
    def __init__(self):
        self.messages = _AnthropicFakeMessagesAPI()


class AnthropicArchitectParsingTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.fake_client = _AnthropicFakeClient()
        anthropic_client.set_client(self.fake_client)

    async def asyncTearDown(self):  # noqa: D401 - cleanup helper
        anthropic_client.set_client(None)

    async def test_parses_text_and_tool_use(self):
        arch = AnthropicArchitect()
        res = await arch.analyze({"ctx": 1}, tools=[{"type": "function", "function": {"name": "web_search", "description": "", "parameters": {"type": "object", "properties": {}}}}])
        self.assertEqual(res.get("findings"), "analysis")
        self.assertIsNotNone(res.get("tool_calls"))
        tc = res["tool_calls"][0]
        self.assertEqual(tc["name"], "web_search")
