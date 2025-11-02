from __future__ import annotations

from typing import Any, BinaryIO, TextIO, overload

def dumps(obj: Any, *, sort_keys: bool = ...) -> str: ...

@overload
def dump(obj: Any, fp: BinaryIO, *, sort_keys: bool = ...) -> None: ...

@overload
def dump(obj: Any, fp: TextIO, *, sort_keys: bool = ...) -> None: ...
