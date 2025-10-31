from typing import Any, Literal, TypedDict

SearchDepth = Literal["basic", "advanced"]

class SearchResponse(TypedDict, total=False):
    results: list[Any]

class AsyncTavilyClient:
    def __init__(self, *, api_key: str) -> None: ...
    async def search(
        self,
        *,
        query: str,
        search_depth: SearchDepth = "basic",
        max_results: int = 5,
        include_images: bool | None = ...,
        include_raw_content: bool | None = ...,
    ) -> SearchResponse: ...

__all__ = ["AsyncTavilyClient", "SearchDepth", "SearchResponse"]
