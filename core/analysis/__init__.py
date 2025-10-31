"""
core/analysis package

This package contains modules for different phases of the project analysis.
"""

# Import all phase analysis classes for easier access
from core.analysis.final_analysis import FinalAnalysis
from core.analysis.phase_1 import Phase1Analysis
from core.analysis.phase_2 import Phase2Analysis
from core.analysis.phase_3 import Phase3Analysis
from core.analysis.phase_4 import Phase4Analysis
from core.analysis.phase_5 import Phase5Analysis

# Export all classes for cleaner imports
__all__ = [
    'Phase1Analysis',
    'Phase2Analysis',
    'Phase3Analysis',
    'Phase4Analysis',
    'Phase5Analysis',
    'FinalAnalysis'
]
