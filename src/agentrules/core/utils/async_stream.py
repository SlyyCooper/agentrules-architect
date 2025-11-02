"""Helpers for adapting synchronous streaming iterators to async generators."""

from __future__ import annotations

import asyncio
import threading
from collections.abc import AsyncIterator, Callable, Iterator
from concurrent.futures import CancelledError
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class _StreamError(Generic[T]):
    error: BaseException


_SENTINEL: object = object()


def iterate_in_thread(iterator_factory: Callable[[], Iterator[T]]) -> AsyncIterator[T]:
    """
    Adapt a blocking iterator into an async iterator using a worker thread.

    Args:
        iterator_factory: Callable returning the synchronous iterator to consume.

    Yields:
        Items produced by the iterator, streamed back onto the event loop.

    Raises:
        Propagates any exception raised by the iterator on the async consumer side.
    """

    loop = asyncio.get_running_loop()
    queue: asyncio.Queue[object] = asyncio.Queue()

    def _runner() -> None:
        try:
            for item in iterator_factory():
                future = asyncio.run_coroutine_threadsafe(queue.put(item), loop)
                future.result()
        except BaseException as exc:  # pragma: no cover - defensive path
            try:
                future = asyncio.run_coroutine_threadsafe(queue.put(_StreamError(error=exc)), loop)
                future.result()
            except (CancelledError, RuntimeError):  # pragma: no cover - loop closed
                pass
        finally:
            try:
                asyncio.run_coroutine_threadsafe(queue.put(_SENTINEL), loop).result()
            except (CancelledError, RuntimeError):  # pragma: no cover - loop closed
                pass

    threading.Thread(target=_runner, daemon=True).start()

    async def _aiter() -> AsyncIterator[T]:
        while True:
            payload = await queue.get()
            if payload is _SENTINEL:
                break
            if isinstance(payload, _StreamError):
                raise payload.error
            yield payload  # type: ignore[misc]

    return _aiter()
