"""
config/prompts/phase_5_prompts.py

This module contains the prompt templates used in Phase 5 (Consolidation) of the project analysis.
These prompts are used by the Anthropic agent to generate the final report.
"""

import json

# Prompt for the Report Agent (Claude)
PHASE_5_PROMPT = """As the Report Agent, create a comprehensive final report from all analysis phases:

Analysis Results:
{results}

Your tasks:
1. Combine all agent findings
2. Organize by component/module
3. Create comprehensive documentation
4. Highlight key discoveries
5. Prepare final report"""

def format_phase5_prompt(results: dict) -> str:
    """
    Format the Phase 5 prompt with the results from all previous phases.

    Args:
        results: Dictionary containing the results from all previous phases

    Returns:
        Formatted prompt string
    """
    return PHASE_5_PROMPT.format(results=json.dumps(results, indent=2))
