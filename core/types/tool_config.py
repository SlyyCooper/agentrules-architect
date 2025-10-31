"""
core/types/tool_config.py

This module defines tool configurations and types for model agent tools.
It provides standard types for defining tools across different model providers.
"""

from typing import Any, Optional, TypedDict


class ToolFunction(TypedDict):
    """Definition of a function tool."""
    name: str
    description: str
    parameters: dict[str, Any]

class Tool(TypedDict):
    """Standard tool definition that can be converted to provider-specific formats."""
    type: str  # Usually "function"
    function: ToolFunction

class ToolConfig(TypedDict):
    """Configuration for tools to be used by models."""
    enabled: bool
    tools: Optional[list[Tool]]

# Provider-specific tool sets
class ToolSets(TypedDict):
    """Tool sets defined for different phases."""
    PHASE_1_TOOLS: Optional[list[Tool]]
    PHASE_2_TOOLS: Optional[list[Tool]]
    PHASE_3_TOOLS: Optional[list[Tool]]
    PHASE_4_TOOLS: Optional[list[Tool]]
    PHASE_5_TOOLS: Optional[list[Tool]]
    FINAL_TOOLS: Optional[list[Tool]]
    RESEARCHER_TOOLS: Optional[list[Tool]]
