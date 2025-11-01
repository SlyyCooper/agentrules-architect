.
├── agentrules/                  # Main application package for the CLI.
│   ├── __init__.py              # Package initializer, silences a specific urllib3 warning.
│   ├── analyzer.py              # Core orchestrator for the multi-phase analysis pipeline.
│   ├── cli/                     # Contains the command-line interface logic using Typer.
│   │   ├── __init__.py          # CLI package initializer.
│   │   ├── app.py               # Defines the main Typer application and registers commands.
│   │   ├── bootstrap.py         # Handles runtime setup like logging and configuration loading.
│   │   ├── commands/            # Directory for Typer subcommands.
│   │   │   ├── __init__.py      # Command package initializer.
│   │   │   ├── analyze.py       # Implements the `analyze` subcommand.
│   │   │   ├── configure.py     # Implements the `configure` subcommand.
│   │   │   └── keys.py          # Implements the `keys` subcommand to show API key status.
│   │   ├── context.py           # Defines a shared context object for the CLI.
│   │   ├── services/            # Business logic for CLI commands.
│   │   │   ├── __init__.py      # Services package initializer.
│   │   │   ├── configuration.py # Service layer for managing application settings.
│   │   │   └── pipeline_runner.py # Service for executing the analysis pipeline.
│   │   └── ui/                  # Contains interactive UI components using `questionary`.
│   │       ├── __init__.py      # UI package initializer.
│   │       ├── analysis_view.py # Renders analysis progress using Rich library components.
│   │       ├── main_menu.py     # Implements the interactive main menu of the CLI.
│   │       ├── settings/        # UI flows for configuring various settings.
│   │       │   ├── __init__.py  # Settings UI package initializer, exports settings modules.
│   │       │   ├── exclusions/  # UI flows for managing file/directory exclusion rules.
│   │       │   │   ├── __init__.py # Manages the main exclusion configuration menu.
│   │       │   │   ├── editor.py # Provides prompts for adding/editing exclusion values.
│   │       │   │   └── summary.py # Renders a summary of current exclusion rules.
│   │       │   ├── logging.py   # UI flow for configuring logging verbosity.
│   │       │   ├── menu.py      # The main settings menu that navigates to other settings pages.
│   │       │   ├── models/      # UI flows for configuring model presets for each phase.
│   │       │   │   ├── __init__.py # Manages the main model configuration menu.
│   │       │   │   ├── researcher.py # UI flow specifically for the researcher agent settings.
│   │       │   │   └── utils.py   # Helper functions for building model selection prompts.
│   │       │   ├── outputs.py   # UI flow for configuring output generation preferences.
│   │       │   └── providers.py # UI flow for managing provider API keys.
│   │       └── styles.py        # Defines custom styles for `questionary` prompts.
│   ├── config_service.py        # Manages loading, saving, and applying user configuration from a TOML file.
│   ├── logging_setup.py         # Configures Rich-based logging handlers and filters.
│   └── model_config.py          # Helpers for managing and applying model preset configurations.
├── config/                      # Contains static configuration for agents, prompts, and tools.
│   ├── __init__.py              # Config package initializer.
│   ├── agents.py                # Defines model configurations and presets for different analysis phases.
│   ├── exclusions.py            # Default exclusion lists for directories, files, and extensions.
│   ├── prompts/                 # Directory for prompt templates.
│   │   ├── __init__.py          # Prompts package initializer.
│   │   ├── final_analysis_prompt.py # Prompt template for the final analysis phase.
│   │   ├── phase_1_prompts.py   # Prompt templates for the initial discovery phase.
│   │   ├── phase_2_prompts.py   # Prompt template for the methodical planning phase.
│   │   ├── phase_3_prompts.py   # Prompt template for the deep analysis phase.
│   │   ├── phase_4_prompts.py   # Prompt template for the synthesis phase.
│   │   └── phase_5_prompts.py   # Prompt template for the consolidation phase.
│   └── tools.py                 # Defines tool configurations available to agents in each phase.
├── conftest.py                  # Pytest configuration file, adds a `--run-live` option.
├── core/                        # Core logic for agents, analysis phases, and utilities.
│   ├── __init__.py              # Core package initializer.
│   ├── agent_tools/             # Tools that can be used by AI agents.
│   │   ├── tool_manager.py      # Manages and converts tool definitions for different providers.
│   │   └── web_search/          # Tools related to web searching.
│   │       ├── __init__.py      # Web search tools package initializer.
│   │       └── tavily.py        # Implements the Tavily web search tool.
│   ├── agents/                  # Contains agent implementations for different AI providers.
│   │   ├── __init__.py          # Agents package initializer with a lazy-loading factory function.
│   │   ├── anthropic/           # Implementation for Anthropic's Claude models.
│   │   │   ├── __init__.py      # Anthropic package initializer.
│   │   │   ├── architect.py     # Main `BaseArchitect` implementation for Anthropic models.
│   │   │   ├── client.py        # Helper for managing the Anthropic SDK client.
│   │   │   ├── prompting.py     # Prompt formatting helpers for Anthropic.
│   │   │   ├── request_builder.py # Constructs API request payloads for Anthropic.
│   │   │   ├── response_parser.py # Parses responses from the Anthropic API.
│   │   │   └── tooling.py       # Helper for preparing tool configurations for Anthropic.
│   │   ├── base.py              # Defines the abstract `BaseArchitect` class for all agents.
│   │   ├── deepseek/            # Implementation for DeepSeek models.
│   │   │   ├── __init__.py      # DeepSeek package initializer.
│   │   │   ├── architect.py     # Main `BaseArchitect` implementation for DeepSeek models.
│   │   │   ├── client.py        # Helper for managing the OpenAI SDK client for DeepSeek.
│   │   │   ├── compat.py        # Backwards-compatible `DeepSeekAgent` wrapper.
│   │   │   ├── config.py        # Model-specific defaults and configuration for DeepSeek.
│   │   │   ├── prompting.py     # Prompt formatting helpers for DeepSeek.
│   │   │   ├── request_builder.py # Constructs API request payloads for DeepSeek.
│   │   │   ├── response_parser.py # Parses responses from the DeepSeek API.
│   │   │   └── tooling.py       # Helper for preparing tool configurations for DeepSeek.
│   │   ├── factory/             # Factory for creating agent instances.
│   │   │   ├── __init__.py      # Factory package initializer.
│   │   │   └── factory.py       # Creates agent instances based on configuration.
│   │   ├── gemini/              # Implementation for Google's Gemini models.
│   │   │   ├── __init__.py      # Gemini package initializer.
│   │   │   ├── architect.py     # Main `BaseArchitect` implementation for Gemini models.
│   │   │   ├── client.py        # Helper for managing the Gemini SDK client.
│   │   │   ├── errors.py        # Custom exceptions for the Gemini provider.
│   │   │   ├── legacy.py        # Backwards-compatible `GeminiAgent` wrapper.
│   │   │   ├── prompting.py     # Prompt formatting helpers for Gemini.
│   │   │   ├── response_parser.py # Parses responses from the Gemini API.
│   │   │   └── tooling.py       # Helper for preparing tool configurations for Gemini.
│   │   ├── openai/              # Implementation for OpenAI models.
│   │   │   ├── __init__.py      # OpenAI package initializer.
│   │   │   ├── architect.py     # Main `BaseArchitect` implementation for OpenAI models.
│   │   │   ├── client.py        # Helper for managing the OpenAI SDK client.
│   │   │   ├── compat.py        # Backwards-compatible `OpenAIAgent` wrapper.
│   │   │   ├── config.py        # Model-specific defaults and configuration for OpenAI.
│   │   │   ├── request_builder.py # Constructs API request payloads for OpenAI.
│   │   │   └── response_parser.py # Parses responses from the OpenAI API.
│   │   └── xai/                 # Implementation for xAI's Grok models.
│   │       ├── __init__.py      # xAI package initializer.
│   │       ├── architect.py     # Main `BaseArchitect` implementation for Grok models.
│   │       ├── client.py        # Helper for managing the OpenAI SDK client for xAI's API.
│   │       ├── config.py        # Model-specific defaults and configuration for xAI.
│   │       ├── prompting.py     # Prompt formatting helpers for xAI.
│   │       ├── request_builder.py # Constructs API request payloads for xAI.
│   │       ├── response_parser.py # Parses responses from the xAI API.
│   │       └── tooling.py       # Helper for preparing tool configurations for xAI.
│   ├── analysis/                # Logic for each phase of the analysis pipeline.
│   │   ├── __init__.py          # Analysis package initializer.
│   │   ├── events.py            # Defines event types for reporting analysis progress.
│   │   ├── final_analysis.py    # Implements the final analysis phase.
│   │   ├── phase_1.py           # Implements the initial discovery phase.
│   │   ├── phase_2.py           # Implements the methodical planning phase.
│   │   ├── phase_3.py           # Implements the deep analysis phase.
│   │   ├── phase_4.py           # Implements the synthesis phase.
│   │   └── phase_5.py           # Implements the consolidation phase.
│   ├── streaming.py             # Defines common data structures for streaming API responses.
│   ├── types/                   # Type definitions and data classes.
│   │   ├── __init__.py          # Types package initializer.
│   │   ├── agent_config.py      # TypedDict for agent phase configurations.
│   │   ├── models.py            # Defines `ModelConfig` and predefined model configurations.
│   │   └── tool_config.py       # TypedDict definitions for agent tools.
│   └── utils/                   # General utility functions.
│       ├── async_stream.py      # Helper to adapt synchronous iterators to async generators.
│       ├── constants.py         # Shared constant values like default filenames.
│       ├── dependency_scanner.py # Scans project files to identify dependencies.
│       ├── file_creation/       # Utilities for creating output files.
│       │   ├── cursorignore.py  # Manages the creation and content of `.cursorignore` files.
│       │   └── phases_output.py # Saves the output of each analysis phase to files.
│       ├── file_system/         # Utilities for interacting with the file system.
│       │   ├── __init__.py      # File system utils package initializer.
│       │   ├── file_retriever.py # Retrieves and formats file contents for analysis.
│       │   ├── gitignore.py     # Helper for loading and applying `.gitignore` patterns.
│       │   └── tree_generator.py # Generates an ASCII tree representation of a directory.
│       ├── formatters/          # Utilities for formatting output files.
│       │   ├── __init__.py      # Formatters package initializer.
│       │   └── clean_cursorrules.py # Cleans the final rules file to ensure correct formatting.
│       ├── model_config_helper.py # Helper to get the name of a model configuration.
│       ├── offline.py           # Provides dummy agent implementations for offline testing.
│       └── parsers/             # Utilities for parsing text and data.
│           ├── __init__.py      # Parsers package initializer.
│           └── agent_parser.py  # Parses agent definitions from Phase 2 XML/text output.
├── main.py                      # Main entry point for running the CLI application.
├── pyproject.toml               # Project metadata, dependencies, and tool configurations.
├── requirements-dev.txt         # Development dependencies for the project.
├── requirements.txt             # Core dependencies for the project.
├── scripts/                     # Utility scripts for development.
│   └── bootstrap_env.sh         # Shell script to set up the development environment.
├── tests/                       # Contains all tests for the project.