from typing import Any

class ThinkingConfig:
    thinking_budget: int | None
    def __init__(self, *, thinking_budget: int | None = ...) -> None: ...

class GenerateContentConfig:
    def __init__(self, **kwargs: Any) -> None: ...

__all__ = ["ThinkingConfig", "GenerateContentConfig"]
