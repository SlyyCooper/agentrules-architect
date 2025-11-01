.
├── __init__.py                # Marks the `core` directory as a Python package.
├── agent_tools/               # Contains tools that AI agents can use.
│   ├── tool_manager.py        # Manages and converts tool definitions for different LLM providers.
│   └── web_search/            # Contains web search tool implementations.
│       ├── __init__.py        # Exports the Tavily web search tool components.
│       └── tavily.py          # Implements a web search tool using the Tavily API.
├── agents/                    # Contains the core logic for different LLM providers (architects).
│   ├── __init__.py            # Exports a factory function for creating architect instances.
│   ├── anthropic/             # Implementation for Anthropic (Claude) models.
│   │   ├── __init__.py        # Exports the AnthropicArchitect class.
│   │   ├── architect.py       # Implements the BaseArchitect interface for Anthropic models.
│   │   ├── client.py          # Helper for creating and using the Anthropic SDK client.
│   │   ├── prompting.py       # Contains prompt formatting logic for Anthropic models.
│   │   ├── request_builder.py # Builds API request payloads for Anthropic models.
│   │   ├── response_parser.py # Parses and normalizes responses from the Anthropic API.
│   │   └── tooling.py         # Handles tool configuration specific to Anthropic models.
│   ├── base.py                # Defines the abstract `BaseArchitect` class and common types.
│   ├── deepseek/              # Implementation for DeepSeek models.
│   │   ├── __init__.py        # Exports the DeepSeekArchitect class and a compatibility wrapper.
│   │   ├── architect.py       # Implements the BaseArchitect interface for DeepSeek models.
│   │   ├── client.py          # Manages OpenAI SDK clients configured for the DeepSeek API.
│   │   ├── compat.py          # Provides a backward-compatible DeepSeekAgent wrapper.
│   │   ├── config.py          # Defines model defaults and configuration for DeepSeek.
│   │   ├── prompting.py       # Contains prompt formatting logic for DeepSeek models.
│   │   ├── request_builder.py # Builds API request payloads for DeepSeek models.
│   │   ├── response_parser.py # Parses and normalizes responses from the DeepSeek API.
│   │   └── tooling.py         # Handles tool configuration specific to DeepSeek models.
│   ├── factory/               # Contains the factory for creating architect instances.
│   │   ├── __init__.py        # Exports the architect factory function.
│   │   └── factory.py         # Creates specific architect instances based on configuration.
│   ├── gemini/                # Implementation for Google Gemini models.
│   │   ├── __init__.py        # Exports the GeminiArchitect class and a compatibility wrapper.
│   │   ├── architect.py       # Implements the BaseArchitect interface for Gemini models.
│   │   ├── client.py          # Helper for creating and using the Gemini SDK client.
│   │   ├── errors.py          # Defines custom exceptions for the Gemini provider.
│   │   ├── legacy.py          # Provides a backward-compatible GeminiAgent wrapper.
│   │   ├── prompting.py       # Contains prompt formatting logic for Gemini models.
│   │   ├── response_parser.py # Parses and normalizes responses from the Gemini API.
│   │   └── tooling.py         # Handles tool configuration specific to Gemini models.
│   ├── openai/                # Implementation for OpenAI models.
│   │   ├── __init__.py        # Exports the OpenAIArchitect class and a compatibility wrapper.
│   │   ├── architect.py       # Implements the BaseArchitect interface for OpenAI models.
│   │   ├── client.py          # Helper for creating and using the OpenAI SDK client.
│   │   ├── compat.py          # Provides a backward-compatible OpenAIAgent wrapper.
│   │   ├── config.py          # Defines model defaults and configuration for OpenAI.
│   │   ├── request_builder.py # Builds API request payloads for OpenAI models.
│   │   └── response_parser.py # Parses and normalizes responses from the OpenAI API.
│   └── xai/                   # Implementation for xAI (Grok) models.
│       ├── __init__.py        # Exports the XaiArchitect class.
│       ├── architect.py       # Implements the BaseArchitect interface for xAI models.
│       ├── client.py          # Manages OpenAI SDK clients configured for the xAI API.
│       ├── config.py          # Defines model defaults and configuration for xAI.
│       ├── prompting.py       # Contains prompt formatting logic for xAI models.
│       ├── request_builder.py # Builds API request payloads for xAI models.
│       ├── response_parser.py # Parses and normalizes responses from the xAI API.
│       └── tooling.py         # Handles tool configuration specific to xAI models.
├── analysis/                  # Contains the logic for each step of the multi-phase analysis.
│   ├── __init__.py            # Exports all analysis phase classes for easy access.
│   ├── events.py              # Defines event types for monitoring the analysis pipeline.
│   ├── final_analysis.py      # Implements the final analysis phase to produce the main output.
│   ├── phase_1.py             # Implements Phase 1: Initial project discovery and research.
│   ├── phase_2.py             # Implements Phase 2: Creates a detailed plan for deep analysis.
│   ├── phase_3.py             # Implements Phase 3: In-depth analysis of code by specialized agents.
│   ├── phase_4.py             # Implements Phase 4: Synthesizes findings from the deep analysis.
│   └── phase_5.py             # Implements Phase 5: Consolidates all findings into a single report.
├── streaming.py               # Defines common data structures for handling streaming API responses.
├── types/                     # Contains shared data type definitions for the project.
│   ├── __init__.py            # Exports key type definitions and model configurations.
│   ├── agent_config.py        # Defines a TypedDict for agent configurations.
│   ├── models.py              # Defines the ModelConfig type and various predefined model settings.
│   └── tool_config.py         # Defines TypedDicts for tool function and configuration structures.
└── utils/                     # Contains various helper utilities for common tasks.
    ├── async_stream.py        # Adapts synchronous, blocking iterators to asynchronous generators.
    ├── constants.py           # Defines shared constants like default output filenames.
    ├── file_creation/         # Utilities for creating project output files.
    │   ├── cursorignore.py    # Manages the creation and modification of .cursorignore files.
    │   └── phases_output.py   # Saves the output of each analysis phase to separate files.
    ├── file_system/           # Utilities for interacting with the file system.
    │   ├── __init__.py        # Exports key file system utility functions.
    │   ├── file_retriever.py  # Retrieves file contents from a directory, respecting exclusions.
    │   ├── gitignore.py       # Loads and applies patterns from .gitignore files.
    │   └── tree_generator.py  # Generates an ASCII tree representation of the project structure.
    ├── formatters/            # Utilities for formatting output files.
    │   ├── __init__.py        # Exports the primary cleaning function.
    │   └── clean_cursorrules.py # Cleans the final output file to ensure correct formatting.
    ├── model_config_helper.py # Helper to get the string name of a model configuration object.
    ├── offline.py             # Provides a dummy architect for running the pipeline without API calls.
    └── parsers/               # Utilities for parsing structured data from LLM responses.
        ├── __init__.py        # Exports key parsing functions.
        └── agent_parser.py    # Parses agent definitions from Phase 2 output using XML and regex.