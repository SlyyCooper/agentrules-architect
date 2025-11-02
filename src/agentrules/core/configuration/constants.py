"""Constants used throughout the configuration subsystem."""

from __future__ import annotations

import logging
import os
from pathlib import Path

from platformdirs import user_config_dir

CONFIG_DIR = Path(os.getenv("AGENTRULES_CONFIG_DIR", user_config_dir("agentrules", "cursorrules")))
CONFIG_FILE = CONFIG_DIR / "config.toml"

DEFAULT_VERBOSITY = "quiet"
VERBOSITY_ENV_VAR = "AGENTRULES_LOG_LEVEL"
VERBOSITY_PRESETS = {
    "quiet": logging.WARNING,
    "standard": logging.INFO,
    "verbose": logging.DEBUG,
}

PROVIDER_ENV_MAP = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "gemini": "GOOGLE_API_KEY",
    "xai": "XAI_API_KEY",
    "tavily": "TAVILY_API_KEY",
}

TRUTHY_ENV_VALUES = {"1", "true", "yes", "on"}

