"""
core/agent_tools/web_search/tavily.py

This module provides the Tavily web search tool implementation.
It includes the tool's schema definition and the function to execute the search.
"""

# ====================================================
# Importing Required Libraries
# ====================================================

import json
import os
from typing import Any, Literal, cast

from tavily import AsyncTavilyClient

from agentrules.core.types.tool_config import Tool

# ====================================================
# Tool Definition
# ====================================================

TAVILY_SEARCH_TOOL_SCHEMA: Tool = cast(Tool, {
    "type": "function",
    "function": {
        "name": "tavily_web_search",
        "description": (
            "Performs a web search using the Tavily API to find up-to-date information. "
            "Returns a list of relevant search results with titles, URLs, and content snippets."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to find information about."
                },
                "search_depth": {
                    "type": "string",
                    "enum": ["basic", "advanced"],
                    "description": (
                        "'basic' for a quick search, 'advanced' for a more in-depth "
                        "search that provides richer content."
                    ),
                    "default": "basic"
                },
                "max_results": {
                    "type": "integer",
                    "description": "The maximum number of search results to return (between 1 and 10).",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    }
})

# Literal type for Tavily depth argument
TavilySearchDepth = Literal["basic", "advanced"]


def _normalize_search_depth(raw_depth: Any) -> TavilySearchDepth:
    """
    Coerce arbitrary input into a valid Tavily search depth literal.
    Defaults to \"basic\" unless the caller explicitly requests \"advanced\".
    """
    if isinstance(raw_depth, str) and raw_depth.lower() == "advanced":
        return "advanced"
    return "basic"


# ====================================================
# Tool Implementation
# ====================================================

async def run_tavily_search(
    query: str,
    search_depth: str = "basic",
    max_results: int = 5
) -> str:
    """
    Asynchronously performs a web search using the Tavily API.

    Args:
        query: The search query.
        search_depth: The depth of the search ('basic' or 'advanced').
        max_results: The maximum number of results to return.

    Returns:
        A JSON string containing the search results or an error message.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return json.dumps({"error": "Tavily API key not found in environment variables."})

    try:
        # Ensure max_results and search depth are within the valid ranges
        clamped_max_results = max(1, min(max_results, 10))
        depth = _normalize_search_depth(search_depth)

        client = AsyncTavilyClient(api_key=api_key)
        response = await client.search(
            query=query,
            search_depth=depth,
            max_results=clamped_max_results
        )
        return json.dumps(response, indent=2)

    except Exception as e:
        return json.dumps({"error": f"An error occurred during the Tavily search: {str(e)}"})
