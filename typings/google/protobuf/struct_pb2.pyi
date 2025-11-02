from typing import Any

class Struct(dict[str, Any]): ...
class Value:
    def WhichOneof(self, name: str) -> str | None: ...

_JSONValue = dict[str, Any]
def DecodeError(*args: Any, **kwargs: Any) -> None: ...

__all__ = ["Struct", "Value", "DecodeError"]
