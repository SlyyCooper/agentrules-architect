"""
tests/final_analysis/test_temporal_framework.py

This script tests the dynamic insertion of the current month and year into the final analysis prompt.
"""

import os
import sys
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agentrules.config.prompts.final_analysis_prompt import format_final_analysis_prompt


def test_temporal_framework():
    """Test that the current month and year are properly inserted into the prompt."""
    # Get current month and year for comparison
    current_date = datetime.now()
    current_month = current_date.strftime("%B")  # Full month name
    current_year = current_date.year

    # Create a simple consolidated report
    consolidated_report = {
        "test": "This is a test report"
    }

    # Format the prompt
    prompt = format_final_analysis_prompt(consolidated_report)

    # Check if the current month and year are in the prompt
    expected_format = f"It is {current_month} {current_year} and [temporal context]"
    expected_example = f"It is {current_month} {current_year} and you are developing with the brand new {current_year}"

    if expected_format in prompt:
        print(f"✅ Format section successfully updated with '{expected_format}'")
    else:
        print(f"❌ Format section not updated correctly. Expected '{expected_format}'")

    if expected_example in prompt:
        print(f"✅ Example section successfully updated with '{expected_example}'")
    else:
        print(f"❌ Example section not updated correctly. Expected '{expected_example}'")

    # Print the relevant sections for visual inspection
    print("\nRelevant sections from the prompt:")
    lines = prompt.split('\n')
    for i, line in enumerate(lines):
        if "It is" in line and (current_month in line or str(current_year) in line):
            start = max(0, i - 5)
            end = min(len(lines), i + 5)
            print("\n".join(lines[start:end]))
            print("-" * 50)

if __name__ == "__main__":
    test_temporal_framework()
