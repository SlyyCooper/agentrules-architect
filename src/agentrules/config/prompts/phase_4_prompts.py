"""
config/prompts/phase_4_prompts.py

This module contains the prompts used by Phase 4 (Synthesis).
Centralizing prompts here makes it easier to edit and maintain them without
modifying the core logic of the agents.
"""

import json

# Prompt template for Phase 4 (Synthesis)
PHASE_4_PROMPT = """Review and synthesize these agent findings:

Analysis Results:
{phase3_results}

Provide:
1. Deep analysis of all findings
2. Methodical processing of new information
3. Updated analysis directions
4. Refined instructions for agents
5. Areas needing deeper investigation"""

def format_phase4_prompt(phase3_results: dict) -> str:
    """
    Format the Phase 4 prompt with the Phase 3 results.

    Args:
        phase3_results: Dictionary containing the results from Phase 3

    Returns:
        Formatted prompt string
    """
    return PHASE_4_PROMPT.format(
        phase3_results=json.dumps(phase3_results, indent=2)
    )
