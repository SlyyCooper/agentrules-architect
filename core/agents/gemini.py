"""
core/agents/gemini.py

This module provides the GeminiArchitect class for interacting with Google's Gemini models.
It handles the creation and execution of agent-based analysis using Gemini models.

This module is used by the main analysis process to perform specialized analysis tasks.
"""

# ====================================================
# Importing Required Libraries
# This section imports all the necessary libraries needed for the script.
# ====================================================

import asyncio  # For async operations
import json  # Used for handling JSON data
import logging  # Used for logging events and errors
import os  # For accessing environment variables
from typing import Any, Optional  # Used for type hinting

from google import genai  # Google GenAI SDK (non-Vertex)
from google.genai import types as genai_types  # Pydantic types
from google.protobuf.struct_pb2 import Struct  # Handle legacy struct args if present

from core.agents.base import BaseArchitect, ModelProvider, ReasoningMode  # Import the base class

# ====================================================
# Initialize the Gemini Client
# This section initializes the client for interacting with the Gemini API.
# ====================================================

# With the new SDK, create a Client per instance (supports API key env discovery)

# ====================================================
# Get Logger
# Set up logger to track events and issues.
# ====================================================

# Get logger
logger = logging.getLogger("project_extractor")


def _collect_candidate_parts(response: Any) -> list[Any]:
    """Safely collect all content parts from a Gemini response."""
    parts: list[Any] = []
    candidates = getattr(response, "candidates", None) or []
    for candidate in candidates:
        content = getattr(candidate, "content", None)
        candidate_parts = getattr(content, "parts", None)
        if not candidate_parts:
            continue
        for part in candidate_parts:
            parts.append(part)
    return parts


def _extract_function_call_args(function_call: Any) -> dict[str, Any]:
    """Normalize Gemini function-call arguments into a dictionary."""
    if function_call is None:
        return {}

    args_obj = getattr(function_call, "args", None)
    if isinstance(args_obj, dict):
        return args_obj
    if isinstance(args_obj, Struct):
        return {key: value for key, value in args_obj.items()}

    arguments_obj = getattr(function_call, "arguments", None)
    if isinstance(arguments_obj, dict):
        return arguments_obj

    return {}

# ====================================================
# GeminiArchitect Class Definition
# This class implements the BaseArchitect for Google's Gemini models.
# ====================================================

class GeminiArchitect(BaseArchitect):
    """
    Architect class for interacting with Google's Gemini models.

    This class provides a structured way to create specialized agents that use
    Gemini models for different analysis tasks. It now supports tool usage.
    """

    # ====================================================
    # Initialization Function (__init__)
    # This function sets up the new GeminiArchitect object when it's created.
    # ====================================================

    def __init__(
        self,
        model_name: str = "gemini-2.0-flash",
        reasoning: ReasoningMode = ReasoningMode.DISABLED,
        name: Optional[str] = None,
        role: Optional[str] = None,
        responsibilities: Optional[list[str]] = None,
        prompt_template: Optional[str] = None,
        api_key: Optional[str] = None,
        tools_config: Optional[dict] = None
    ):
        """
        Initialize a Gemini architect with specific configurations.

        Args:
            model_name: The Gemini model to use
            reasoning: Whether to enable thinking models
            name: Optional name for specialized roles
            role: Optional role description
            responsibilities: Optional list of responsibilities
            prompt_template: Optional custom prompt template
            api_key: Optional API key for Gemini
            tools_config: Optional configuration for tools the model can use
        """
        super().__init__(
            provider=ModelProvider.GEMINI,
            model_name=model_name,
            reasoning=reasoning,
            name=name,
            role=role,
            responsibilities=responsibilities,
            tools_config=tools_config
        )
        self.prompt_template = prompt_template or self._get_default_prompt_template()

        # Try to get the API key from environment variable if not provided
        if api_key is None:
            api_key = os.environ.get("GEMINI_API_KEY")

        # Initialize the Google GenAI Client
        # The client picks API key from GEMINI_API_KEY or GOOGLE_API_KEY automatically.
        # Allow explicit override via parameter for clarity/testing.
        try:
            self.client = genai.Client(api_key=api_key) if api_key else genai.Client()
        except Exception:
            # Defer errors to call-site where we can surface a clear message
            self.client = None

    # ====================================================
    # Default Prompt Template Function (_get_default_prompt_template)
    # This function returns the default prompt template for the agent.
    # ====================================================

    def _get_default_prompt_template(self) -> str:
        """Get the default prompt template for the agent."""
        return """You are the {agent_name}, responsible for {agent_role}.

        Your specific responsibilities are:
        {agent_responsibilities}

        Analyze this project context and provide a detailed report focused on your domain:

        {context}

        Format your response as a structured report with clear sections and findings."""

    # ====================================================
    # Prompt Formatting Function (format_prompt)
    # This function formats the prompt with specific agent information and context.
    # ====================================================

    def format_prompt(self, context: dict[str, Any]) -> str:
        """
        Format the prompt template with the agent's information and context.

        Args:
            context: Dictionary containing the context for analysis

        Returns:
            Formatted prompt string
        """
        responsibilities_str = "\n".join(f"- {r}" for r in self.responsibilities)
        context_str = json.dumps(context, indent=2)

        return self.prompt_template.format(
            agent_name=self.name or "Gemini Architect",
            agent_role=self.role or "analyzing the project",
            agent_responsibilities=responsibilities_str,
            context=context_str
        )

    # ====================================================
    # Analysis Function (analyze)
    # This function sends a request to the Gemini API and processes the response.
    # ====================================================

    async def analyze(self, context: dict, tools: Optional[list[Any]] = None) -> dict:
        """
        Run agent analysis using Gemini model, potentially using tools.

        Args:
            context: Dictionary containing the context for analysis
            tools: Optional list of tools the model can use.
                   Provide as `google.genai.types.Tool` instances or as dictionaries
                   adhering to the Gemini function declaration schema.

        Returns:
            Dictionary containing the agent's findings, potential function calls, or error information
        """
        try:
            if not self.client:
                raise ValueError("Gemini client not initialized. Please provide an API key.")

            # Check if the context already contains a formatted prompt
            if "formatted_prompt" in context:
                prompt = context["formatted_prompt"]
            else:
                # Format the prompt using the template
                prompt = self.format_prompt(context)

            # Configure model parameters based on model and reasoning mode
            model_name = self.model_name

            # Thinking is controlled via thinking_config in GenerateContentConfig

            # Build GenerateContentConfig per new SDK
            config_kwargs: dict[str, Any] = {}
            # System instruction as a string
            if self.role:
                config_kwargs["system_instruction"] = (
                    f"You are {self.name or 'an AI assistant'}, responsible for {self.role}."
                )
            # Tools
            api_tools = None
            if tools or (self.tools_config and self.tools_config.get("enabled", False)):
                tool_list = tools or self.tools_config.get("tools", [])
                if tool_list:
                    from core.agent_tools.tool_manager import ToolManager
                    api_tools = ToolManager.get_provider_tools(tool_list, ModelProvider.GEMINI)
                    if api_tools:
                        config_kwargs["tools"] = api_tools
            # Thinking config when reasoning is enabled
            if self.reasoning == ReasoningMode.ENABLED:
                config_kwargs["thinking_config"] = genai_types.ThinkingConfig(thinking_budget=16000)
            generation_config = genai_types.GenerateContentConfig(**config_kwargs) if config_kwargs else None

            # Get the model configuration name
            from core.utils.model_config_helper import get_model_config_name
            model_config_name = get_model_config_name(self)

            agent_name = self.name or "Gemini Architect"
            details: list[str] = []
            if self.reasoning == ReasoningMode.ENABLED:
                details.append("with thinking")
            if api_tools:
                details.append("with tools enabled")
            detail_suffix = f" ({', '.join(details)})" if details else ""
            logger.info(
                f"[bold magenta]{agent_name}:[/bold magenta] Sending request to {model_name} "
                f"(Config: {model_config_name}){detail_suffix}"
            )

            # Send a request to the Gemini API to analyze the given context.
            client = self.client
            if client is None:
                raise ValueError("Gemini client not initialized. Please provide a valid API key or set GEMINI_API_KEY.")
            response = await asyncio.to_thread(
                client.models.generate_content,
                model=model_name,
                contents=prompt,
                config=generation_config,
            )

            logger.info(f"[bold green]{agent_name}:[/bold green] Received response from {model_name}")

            # Process the response
            results = {
                "agent": agent_name,
                "findings": None,
                "function_calls": None # Use 'function_calls' for Gemini
            }

            # Extract text part
            parts = _collect_candidate_parts(response)

            try:
                results["findings"] = response.text
            except ValueError:
                results["findings"] = None

            if not results["findings"]:
                for part in parts:
                    part_text = getattr(part, "text", None)
                    if part_text:
                        results["findings"] = part_text
                        break
                else:
                    logger.warning(f"{agent_name}: No direct text content found in response.")

            # Extract function calls
            function_calls = []
            for part in parts:
                fc = getattr(part, "function_call", None)
                if fc is None:
                    continue
                function_calls.append({
                    "name": getattr(fc, "name", None),
                    "args": _extract_function_call_args(fc),
                })

            if function_calls:
                 logger.info(f"[bold magenta]{agent_name}:[/bold magenta] Model requested function call(s).")
                 results["function_calls"] = function_calls
                 # Clear findings if only function calls are present and no text was extracted
                 if not results["findings"]:
                      results["findings"] = None

            return results

        except Exception as e:
            agent_name = self.name or "Gemini Architect"
            logger.error(f"[bold red]Error in {agent_name}:[/bold red] {str(e)}")
            # Return an error message if something goes wrong.
            return {
                "agent": agent_name,
                "error": str(e)
            }

    # ====================================================
    # Create Analysis Plan - Not primary function but implemented for compatibility
    # ====================================================
    async def create_analysis_plan(self, phase1_results: dict, prompt: Optional[str] = None) -> dict:
        """
        Create an analysis plan based on Phase 1 results.
        (Does not currently support tool usage for this specific task)

        This is implemented for compatibility with the base class but not the
        primary function of the Gemini model in the current architecture.

        Args:
            phase1_results: Dictionary containing the results from Phase 1
            prompt: Optional custom prompt to use

        Returns:
            Dictionary containing the analysis plan
        """
        context: dict[str, Any] = {"phase1_results": phase1_results}
        if prompt:
            context["formatted_prompt"] = prompt
        # Call analyze without tools
        result = await self.analyze(context)

        return {
            "plan": result.get("findings", "No plan generated"),
            "error": result.get("error", None)
        }

    # ====================================================
    # Synthesize Findings - Not primary function but implemented for compatibility
    # ====================================================
    async def synthesize_findings(self, phase3_results: dict, prompt: Optional[str] = None) -> dict:
        """
        Synthesize findings from Phase 3.
        (Does not currently support tool usage for this specific task)

        This is implemented for compatibility with the base class but not the
        primary function of the Gemini model in the current architecture.

        Args:
            phase3_results: Dictionary containing the results from Phase 3
            prompt: Optional custom prompt to use

        Returns:
            Dictionary containing the synthesis
        """
        context: dict[str, Any] = {"phase3_results": phase3_results}
        if prompt:
            context["formatted_prompt"] = prompt
        # Call analyze without tools
        result = await self.analyze(context)

        return {
            "analysis": result.get("findings", "No synthesis generated"),
            "error": result.get("error", None)
        }

    # ====================================================
    # Final Analysis - Not primary function but implemented for compatibility
    # ====================================================
    async def final_analysis(self, consolidated_report: dict, prompt: Optional[str] = None) -> dict:
        """
        Perform final analysis on the consolidated report.
        (Does not currently support tool usage for this specific task)

        This is implemented for compatibility with the base class but not the
        primary function of the Gemini model in the current architecture.

        Args:
            consolidated_report: Dictionary containing the consolidated report
            prompt: Optional custom prompt to use

        Returns:
            Dictionary containing the final analysis
        """
        context: dict[str, Any] = {"consolidated_report": consolidated_report}
        if prompt:
            context["formatted_prompt"] = prompt
        # Call analyze without tools
        result = await self.analyze(context)

        return {
            "analysis": result.get("findings", "No final analysis generated"),
            "error": result.get("error", None)
        }

    # ====================================================
    # Consolidate Results - Primary method for Phase 5
    # ====================================================
    async def consolidate_results(self, all_results: dict, prompt: Optional[str] = None) -> dict:
        """
        Consolidate results from all previous phases.
        (Does not currently support tool usage for this specific task)

        Args:
            all_results: Dictionary containing all phase results
            prompt: Optional custom prompt to use

        Returns:
            Dictionary containing the consolidated report
        """
        try:
            # Use the provided prompt or format a default one
            content = prompt or (
                "Consolidate these results into a comprehensive report:\n\n"
                f"{json.dumps(all_results, indent=2)}"
            )

            # Configure model parameters
            model_name = self.model_name

            # Check if we should use a thinking model
            if self.reasoning == ReasoningMode.ENABLED:
                 # Use the thinking variant of the selected model
                if "gemini-2.0-flash" in model_name:
                    model_name = "gemini-2.0-flash-thinking-exp"
                elif "gemini-2.5-pro" in model_name:
                    model_name = "gemini-2.5-pro-exp-03-25"

            # Use the same models.generate_content path as in analyze()
            client = self.client
            if client is None:
                raise ValueError("Gemini client not initialized. Please provide a valid API key or set GEMINI_API_KEY.")
            response = await asyncio.to_thread(
                client.models.generate_content,
                model=model_name,
                contents=content,
            )

            # Return the consolidated report
            return {"phase": "Consolidation", "report": response.text}
        except Exception as e:
            logger.error(f"Error in consolidation: {str(e)}")
            return {
                "phase": "Consolidation",
                "error": str(e)
            }

# ====================================================
# Legacy GeminiAgent Class
# Maintained for backward compatibility
# ====================================================

class GeminiAgent:
    """
    Agent class for interacting with Google's Gemini models.

    This class provides a structured way to create specialized agents that use
    Gemini models for different analysis tasks.

    Note: This class is maintained for backward compatibility. New code should use
    GeminiArchitect instead.
    """

    def __init__(
        self,
        name: str,
        role: str,
        responsibilities: list[str],
        prompt_template: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        """
        Initialize a Gemini agent with a specific name, role, and responsibilities.

        Args:
            name: The name of the agent (e.g., "Structure Agent")
            role: The role of the agent (e.g., "analyzing directory and file organization")
            responsibilities: A list of specific tasks the agent is responsible for
            prompt_template: Optional custom prompt template to use instead of the default
            api_key: Optional API key for Gemini
        """
        self.name = name
        self.role = role
        self.responsibilities = responsibilities

        # Store the provided prompt template first
        self._provided_prompt_template = prompt_template

        self._architect = GeminiArchitect(
            name=name,
            role=role,
            responsibilities=responsibilities,
            prompt_template=prompt_template,
            api_key=api_key,
            tools_config=None # Legacy agent does not support tools
        )

        # Now initialize the prompt_template properly
        self.prompt_template = prompt_template or self._get_default_prompt_template()

    def _get_default_prompt_template(self) -> str:
        """Get the default prompt template for the agent."""
        # Always delegate to the architect to get the default template
        return self._architect._get_default_prompt_template()

    def format_prompt(self, context: dict[str, Any]) -> str:
        """
        Format the prompt template with the agent's information and context.

        Args:
            context: Dictionary containing the context for analysis

        Returns:
            Formatted prompt string
        """
        return self._architect.format_prompt(context)

    # Note: Legacy analyze method doesn't pass 'tools'
    async def analyze(self, context: dict) -> dict:
        """
        Run agent analysis using Gemini model.

        Args:
            context: Dictionary containing the context for analysis

        Returns:
            Dictionary containing the agent's findings or error information
        """
        return await self._architect.analyze(context) # Call architect's analyze without tools
