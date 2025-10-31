```
.
├── __init__.py                # Exposes a public factory function to create architect instances.
├── anthropic/                 # Contains the implementation for the Anthropic (Claude) model provider.
│   ├── __init__.py            # Exposes the AnthropicArchitect class for public use.
│   ├── architect.py           # Implements the BaseArchitect interface for Anthropic models.
│   ├── client.py              # Manages the Anthropic SDK client instance and request execution.
│   ├── prompting.py           # Provides prompt templating and formatting for Anthropic models.
│   ├── request_builder.py     # Constructs API request payloads for Anthropic's Messages API.
│   ├── response_parser.py     # Parses and normalizes responses from the Anthropic API.
│   ├── tooling.py             # Handles tool configuration and formatting for Anthropic models.
├── base.py                    # Defines the abstract BaseArchitect class and core enums.
├── deepseek/                  # Contains the implementation for the DeepSeek model provider.
│   ├── __init__.py            # Exposes the DeepSeekArchitect class and a legacy agent.
│   ├── architect.py           # Implements the BaseArchitect interface for DeepSeek models.
│   ├── client.py              # Manages OpenAI SDK clients configured for DeepSeek's API endpoint.
│   ├── compat.py              # Provides a backward-compatibility wrapper for a legacy agent class.
│   ├── config.py              # Defines model-specific defaults and configuration for DeepSeek.
│   ├── prompting.py           # Provides prompt templating and formatting for DeepSeek models.
│   ├── request_builder.py     # Constructs API request payloads for DeepSeek's chat completions API.
│   ├── response_parser.py     # Parses and normalizes responses from the DeepSeek API.
│   ├── tooling.py             # Handles tool configuration and formatting for DeepSeek models.
├── factory/                   # Contains the factory for creating different architect instances.
│   ├── __init__.py            # Exposes the architect factory function.
│   ├── factory.py             # Implements the factory pattern to instantiate provider-specific architects.
├── gemini/                    # Contains the implementation for the Google Gemini model provider.
│   ├── __init__.py            # Exposes the GeminiArchitect and legacy agent classes.
│   ├── architect.py           # Implements the BaseArchitect interface for Gemini models.
│   ├── client.py              # Manages the Google GenAI client and asynchronous request execution.
│   ├── errors.py              # Defines custom exception types for the Gemini provider.
│   ├── legacy.py              # Provides a backward-compatibility wrapper for a legacy agent class.
│   ├── prompting.py           # Provides prompt templating and formatting for Gemini models.
│   ├── response_parser.py     # Parses and normalizes responses from the Gemini API.
│   ├── tooling.py             # Handles tool configuration and formatting for Gemini models.
├── openai/                    # Contains the implementation for the OpenAI model provider.
│   ├── __init__.py            # Exposes the OpenAIArchitect and legacy agent classes.
│   ├── architect.py           # Implements the BaseArchitect interface for OpenAI models.
│   ├── client.py              # Manages the OpenAI SDK client instance and request execution.
│   ├── compat.py              # Provides a backward-compatibility wrapper for a legacy agent class.
│   ├── config.py              # Defines model-specific defaults and configuration for OpenAI.
│   ├── request_builder.py     # Constructs API request payloads for OpenAI's Chat and Responses APIs.
│   ├── response_parser.py     # Parses and normalizes responses from the OpenAI API.
├── xai/                       # Contains the implementation for the xAI (Grok) model provider.
│   ├── __init__.py            # Exposes the XaiArchitect class for public use.
│   ├── architect.py           # Implements the BaseArchitect interface for xAI models.
│   ├── client.py              # Manages OpenAI SDK clients configured for xAI's API endpoint.
│   ├── config.py              # Defines model-specific defaults and configuration for xAI.
│   ├── prompting.py           # Provides prompt templating and formatting for xAI models.
│   ├── request_builder.py     # Constructs API request payloads for xAI's chat completions API.
│   ├── response_parser.py     # Parses and normalizes responses from the xAI API.
│   ├── tooling.py             # Handles tool configuration and formatting for xAI models.
```