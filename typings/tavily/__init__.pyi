from typing import Any, Literal, Optional, TypedDict

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
        include_images: Optional[bool] = ...,
        include_raw_content: Optional[bool] = ...,
    ) -> SearchResponse: ...

__all__ = ["AsyncTavilyClient", "SearchDepth", "SearchResponse"]
