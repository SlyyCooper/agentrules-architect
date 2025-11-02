"""
OpenAI agent package.

This package exposes the public OpenAI architect surface while organising the
implementation into focused modules for request construction, SDK dispatch,
and response parsing.
"""

from .architect import OpenAIArchitect
from .compat import OpenAIAgent

__all__ = ["OpenAIArchitect", "OpenAIAgent"]

