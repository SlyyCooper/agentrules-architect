#!/usr/bin/env python3
"""
utils/file_creation/cursorignore.py

This module provides functionality for managing .cursorignore files in a project.
It allows creating, adding patterns to, and removing patterns from .cursorignore files.

This module is used by the project analysis phases to manage which files should be
ignored by Cursor AI.
"""

# ====================================================
# Importing Required Libraries
# This section imports all the necessary libraries needed for the script.
# ====================================================

import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import Optional

# ====================================================
# Constants
# This section defines constant variables used throughout the script.
# ====================================================
CURSORIGNORE_FILE = ".cursorignore"  # Default name for the .cursorignore file
PATTERNS_FILE = os.path.join(str(Path.home()), ".ci_saved_patterns")  # Path to save patterns


# ====================================================
# Function: show_help
# This function returns the help text explaining how to use the script.
# ====================================================
def show_help() -> str:
    """Return help text for the cursorignore functionality."""
    return """Usage: cursorignore [OPTIONS]
Manage .cursorignore file in the current directory.

Without options: creates a .cursorignore file with saved patterns

Options:
  --add PATTERN    Add a pattern to .cursorignore and save it
  --remove PATTERN Remove a pattern from .cursorignore and saved patterns
  --list           List all saved patterns
  --help           Display this help message"""


# ====================================================
# Function: initialize_patterns_file
# This function creates the file that stores saved patterns if it doesn't exist.
# ====================================================
def initialize_patterns_file() -> None:
    """Initialize the patterns file if it doesn't exist."""
    if not os.path.isfile(PATTERNS_FILE):
        with open(PATTERNS_FILE, 'w'):
            pass  # Create empty file


# ====================================================
# Function: get_saved_patterns
# This function retrieves all saved patterns from the patterns file.
# ====================================================
def get_saved_patterns() -> list[str]:
    """Get all saved patterns from the patterns file."""
    initialize_patterns_file()

    if not os.path.getsize(PATTERNS_FILE) > 0:
        return []

    with open(PATTERNS_FILE) as f:
        return [line.strip() for line in f.readlines()]


# ====================================================
# Function: list_patterns
# This function lists all currently saved patterns.
# ====================================================
def list_patterns() -> tuple[bool, str]:
    """List all saved patterns.

    Returns:
        Tuple[bool, str]: Success status and message
    """
    patterns = get_saved_patterns()

    if not patterns:
        return True, "No patterns are currently saved"

    return True, "Saved patterns:\n" + "\n".join(patterns)


# ====================================================
# Function: create_cursorignore
# This function creates a .cursorignore file in the specified directory,
# populating it with saved patterns if any exist.
# ====================================================
def create_cursorignore(directory: Optional[str] = None) -> tuple[bool, str]:
    """Create a .cursorignore file with saved patterns if it doesn't exist.

    Args:
        directory: Optional directory path where to create the file. If None, uses current directory.

    Returns:
        Tuple[bool, str]: Success status and message
    """
    # Determine the full path for the .cursorignore file
    if directory:
        cursorignore_path = os.path.join(directory, CURSORIGNORE_FILE)
    else:
        cursorignore_path = CURSORIGNORE_FILE

    if os.path.isfile(cursorignore_path):
        return True, f".cursorignore file already exists at {cursorignore_path}"

    patterns = get_saved_patterns()

    with open(cursorignore_path, 'w') as f:
        if patterns:
            f.write("\n".join(patterns) + "\n")
            return True, f"Created .cursorignore file with saved patterns at {cursorignore_path}"
        else:
            return True, f"Created empty .cursorignore file at {cursorignore_path} (no saved patterns)"


# ====================================================
# Function: pattern_exists
# This function checks if a specific pattern already exists in a given file.
# ====================================================
def pattern_exists(pattern: str, file_path: str) -> bool:
    """Check if a pattern exists in a file.

    Args:
        pattern: The pattern to check for
        file_path: The file to check in

    Returns:
        bool: True if pattern exists, False otherwise
    """
    if not os.path.isfile(file_path):
        return False

    with open(file_path) as f:
        content = f.read()
        # Use regex to match the exact pattern on a line
        return bool(re.search(f"^{re.escape(pattern)}$", content, re.MULTILINE))


# ====================================================
# Function: add_pattern
# This function adds a new pattern to both the .cursorignore file
# and the saved patterns file.
# ====================================================
def add_pattern(pattern: str) -> tuple[bool, str]:
    """Add a pattern to .cursorignore and save it.

    Args:
        pattern: The pattern to add

    Returns:
        Tuple[bool, str]: Success status and message
    """
    if not pattern:
        return False, "Error: No pattern specified to add\nUsage: cursorignore --add PATTERN"

    messages = []

    # Add to saved patterns if not already there
    if not pattern_exists(pattern, PATTERNS_FILE):
        with open(PATTERNS_FILE, 'a') as f:
            f.write(f"{pattern}\n")
        messages.append(f"Added '{pattern}' to saved patterns")
    else:
        messages.append(f"Pattern '{pattern}' is already in saved patterns")

    # Create or update .cursorignore file if it exists
    if os.path.isfile(CURSORIGNORE_FILE):
        if not pattern_exists(pattern, CURSORIGNORE_FILE):
            with open(CURSORIGNORE_FILE, 'a') as f:
                f.write(f"{pattern}\n")
            messages.append(f"Added '{pattern}' to .cursorignore")
        else:
            messages.append(f"Pattern '{pattern}' already exists in .cursorignore")

    return True, "\n".join(messages)


# ====================================================
# Function: remove_pattern_from_file
# This function removes a specified pattern from a given file.
# ====================================================
def remove_pattern_from_file(pattern: str, file_path: str) -> bool:
    """Remove a pattern from a file.

    Args:
        pattern: The pattern to remove
        file_path: The file to remove from

    Returns:
        bool: True if pattern was removed, False otherwise
    """
    if not os.path.isfile(file_path):
        return False

    if not pattern_exists(pattern, file_path):
        return False

    # Create a temporary file
    fd, temp_path = tempfile.mkstemp()
    try:
        with os.fdopen(fd, 'w') as temp_file:
            with open(file_path) as source_file:
                for line in source_file:
                    if line.strip() != pattern:
                        temp_file.write(line)

        # Replace the original file with the temp file
        shutil.move(temp_path, file_path)
        return True
    except Exception:
        # If something goes wrong, make sure we clean up the temp file
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        return False


# ====================================================
# Function: remove_pattern
# This function removes a pattern from both the .cursorignore file
# and the saved patterns file.
# ====================================================
def remove_pattern(pattern: str) -> tuple[bool, str]:
    """Remove a pattern from .cursorignore and saved patterns.

    Args:
        pattern: The pattern to remove

    Returns:
        Tuple[bool, str]: Success status and message
    """
    if not pattern:
        return False, "Error: No pattern specified to remove\nUsage: cursorignore --remove PATTERN"

    messages = []

    # Remove from saved patterns
    if remove_pattern_from_file(pattern, PATTERNS_FILE):
        messages.append(f"Removed '{pattern}' from saved patterns")
    else:
        messages.append(f"Pattern '{pattern}' not found in saved patterns")

    # Also remove from current .cursorignore if it exists
    if os.path.isfile(CURSORIGNORE_FILE):
        if remove_pattern_from_file(pattern, CURSORIGNORE_FILE):
            messages.append(f"Removed '{pattern}' from .cursorignore")

    return True, "\n".join(messages)


# ====================================================
# Function: process_command
# This function processes the command-line arguments and calls the appropriate functions.
# ====================================================
def process_command(args: Optional[list[str]] = None) -> tuple[bool, str]:
    """Process a cursorignore command.

    Args:
        args: Command line arguments (optional)

    Returns:
        Tuple[bool, str]: Success status and message
    """
    if args is None or len(args) == 0:
        return create_cursorignore()

    command = args[0]

    if command == "--help":
        return True, show_help()
    elif command == "--list":
        return list_patterns()
    elif command == "--add" and len(args) > 1:
        return add_pattern(args[1])
    elif command == "--remove" and len(args) > 1:
        return remove_pattern(args[1])
    else:
        return False, f"Error: Invalid option '{command}'\n{show_help()}"
