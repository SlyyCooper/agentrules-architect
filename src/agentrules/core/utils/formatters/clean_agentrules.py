#!/usr/bin/env python3
"""
core/utils/formatters/clean_agentrules.py

This module provides functionality for cleaning the generated rules file by
removing any text before the first occurrence of "You are...".

This ensures that agent rules files start with the proper system prompt format.
"""

# ====================================================
# Importing Required Libraries
# ====================================================

import os
import re

from agentrules.core.utils.constants import DEFAULT_RULES_FILENAME

# ====================================================
# Constants
# ====================================================
START_PATTERN = re.compile(r'\bYou are\b', re.IGNORECASE)  # Pattern to find "You are" text


# ====================================================
# Function: clean_agentrules_file
# This function cleans the AGENTS.md rules file by removing any text
# before the first occurrence of "You are..."
# ====================================================
def clean_agentrules_file(file_path: str) -> tuple[bool, str]:
    """
    Clean the rules file by removing any text before "You are...".

    Args:
        file_path: Path to the generated rules file

    Returns:
        Tuple[bool, str]: Success status and message
    """
    try:
        # Check if file exists
        if not os.path.isfile(file_path):
            return False, f"File not found: {file_path}"

        # Read file content
        with open(file_path, encoding='utf-8') as f:
            content = f.read()

        # Find first occurrence of "You are"
        match = START_PATTERN.search(content)
        if not match:
            return False, f"Pattern 'You are' not found in {file_path}"

        # Get the cleaned content starting from "You are"
        cleaned_content = content[match.start():]

        # Write the cleaned content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)

        return True, f"Successfully cleaned {file_path}"

    except Exception as e:
        return False, f"Error cleaning {file_path}: {str(e)}"


# ====================================================
# Function: clean_agentrules
# This function finds and cleans an AGENTS.md rules file in the specified directory
# ====================================================
def clean_agentrules(directory: str | None = None, *, filename: str | None = None) -> tuple[bool, str]:
    """
    Find and clean an AGENTS.md rules file in the specified directory.

    Args:
        directory: Optional directory path where to find the file. If None, uses current directory.

    Returns:
        Tuple[bool, str]: Success status and message
    """
    # Determine the full path for the rules file
    target_filename = filename or DEFAULT_RULES_FILENAME
    if directory:
        agentrules_path = os.path.join(directory, target_filename)
    else:
        agentrules_path = target_filename

    return clean_agentrules_file(agentrules_path)
