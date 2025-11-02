"""
Lightweight fake response objects that mimic vendor SDK shapes used in the code.

These keep tests fully offline and stable without incurring API charges.
"""

from typing import Any

# -------------------------------
# OpenAI / DeepSeek (OpenAI-style)
# -------------------------------

class _ToolFunctionFake:
    def __init__(self, name: str, arguments: str) -> None:
        self.name = name
        self.arguments = arguments  # JSON string per SDK


class _ToolCallFake:
    def __init__(self, call_id: str, name: str, arguments: str) -> None:
        self.id = call_id
        self.type = "function"
        self.function = _ToolFunctionFake(name=name, arguments=arguments)


class _MessageFake:
    def __init__(self, content: str | None, tool_calls: list[_ToolCallFake] | None = None, reasoning_content: str | None = None) -> None:
        self.content = content
        self.tool_calls = tool_calls or []
        # DeepSeek reasoner extension
        if reasoning_content is not None:
            self.reasoning_content = reasoning_content


class _ChoiceFake:
    def __init__(self, message: _MessageFake) -> None:
        self.message = message


class OpenAIChatCompletionFake:
    def __init__(self, content: str | None = "Hello", tool_calls: list[_ToolCallFake] | None = None) -> None:
        self.choices = [_ChoiceFake(_MessageFake(content=content, tool_calls=tool_calls))]


class DeepSeekChatCompletionFake:
    def __init__(self, content: str | None = "Hi from DeepSeek", tool_calls: list[_ToolCallFake] | None = None, reasoning: str | None = None) -> None:
        self.choices = [_ChoiceFake(_MessageFake(content=content, tool_calls=tool_calls, reasoning_content=reasoning))]


# ---------
# Anthropic
# ---------

class _AnthropicToolUse:
    def __init__(self, tool_id: str, name: str, input_data: Any) -> None:
        self.id = tool_id
        self.name = name
        self.input = input_data


class _AnthropicTextBlock:
    def __init__(self, text: str) -> None:
        self.type = "text"
        self.text = text


class _AnthropicToolUseBlock:
    def __init__(self, tool_id: str, name: str, input_data: Any) -> None:
        # Anthropic SDK exposes a `tool_use` content block, we emulate it
        self.type = "tool_use"
        self.id = tool_id
        self.name = name
        self.input = input_data
        self.tool_use = _AnthropicToolUse(tool_id, name, input_data)


class AnthropicMessageCreateResponseFake:
    def __init__(self, text: str | None = None, tool_call: _AnthropicToolUseBlock | None = None) -> None:
        blocks: list[Any] = []
        if text is not None:
            blocks.append(_AnthropicTextBlock(text))
        if tool_call is not None:
            blocks.append(tool_call)
        self.content = blocks


# ------
# Gemini
# ------

class _FunctionCallFake:
    def __init__(self, name: str, args: Any) -> None:
        self.name = name
        self.args = args


class _PartFake:
    def __init__(self, text: str | None = None, function_call: _FunctionCallFake | None = None) -> None:
        self.text = text
        self.function_call = function_call


class _ContentFake:
    def __init__(self, parts: list[_PartFake]) -> None:
        self.parts = parts


class _CandidateFake:
    def __init__(self, parts: list[_PartFake]) -> None:
        self.content = _ContentFake(parts)


class GeminiGenerateContentResponseFake:
    def __init__(self, text: str | None = None, function_call: _FunctionCallFake | None = None) -> None:
        # Some responses provide `.text`; others require reading from parts
        self.text = text or ""
        parts = []
        if text:
            parts.append(_PartFake(text=text))
        if function_call:
            parts.append(_PartFake(function_call=function_call))
        self.candidates = [_CandidateFake(parts)]
