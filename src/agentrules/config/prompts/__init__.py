"""
config/prompts package

This package contains prompt templates for different phases of the project analysis.
"""

# Import all prompt modules for easy access
from agentrules.config.prompts.final_analysis_prompt import *
from agentrules.config.prompts.phase_1_prompts import *
from agentrules.config.prompts.phase_2_prompts import *

# phase_3_prompts removed - now implemented directly in phase_3.py
from agentrules.config.prompts.phase_4_prompts import *
from agentrules.config.prompts.phase_5_prompts import *
