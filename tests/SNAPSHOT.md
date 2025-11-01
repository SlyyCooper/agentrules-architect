│   .
│   ├── __init__.py              # Tests package initializer.
│   ├── fakes/                   # Fake objects for testing.
│   │   └── vendor_responses.py  # Fake response objects mimicking vendor SDKs for offline tests.
│   ├── final_analysis_test/     # Tests for the final analysis phase.
│   │   ├── __init__.py          # Test package initializer.
│   │   ├── output/              # Directory for final analysis test outputs.
│   │   ├── run_test.py          # Script to run an offline test of the final analysis phase.
│   │   ├── test_date.py         # Tests the dynamic date insertion in the final analysis prompt.
│   │   ├── test_final_analysis.py # Live tests for the final analysis phase against various models.
│   │   └── test_final_offline.py # Offline unit test for the final analysis phase.
│   ├── live/                    # Live integration tests that hit external APIs.
│   │   └── test_live_smoke.py   # A simple smoke test for the final analysis with the default live provider.
│   ├── offline/                 # Offline integration tests.
│   │   ├── __init__.py          # Test package initializer.
│   │   └── test_offline_smoke.py # Offline smoke tests for various analysis phases.
│   ├── phase_1_test/            # Tests for the initial discovery phase.
│   │   ├── __init__.py          # Test package initializer.
│   │   ├── output/              # Directory for phase 1 test outputs.
│   │   ├── run_test.py          # Script to run an offline test of the discovery phase.
│   │   ├── test_phase1_offline.py # Offline unit test for the discovery phase.
│   │   └── test_phase1_researcher_guards.py # Unit tests for researcher agent logic (e.g., tool handling).
│   ├── phase_2_test/            # Tests for the methodical planning phase.
│   │   ├── __init__.py          # Test package initializer.
│   │   ├── output/              # Directory for phase 2 test outputs.
│   │   │   └── analysis_plan.xml # Example output of an analysis plan from a test run.
│   │   ├── run_test.py          # Script to run an offline test of the planning phase.
│   │   └── test_phase2_offline.py # Offline unit test for the planning phase.
│   ├── phase_3_test/            # Tests for the deep analysis phase.
│   │   ├── __init__.py          # Test package initializer.
│   │   ├── debug_parser.py      # Debugging script for the agent parser.
│   │   ├── output/              # Directory for phase 3 test outputs.
│   │   ├── run_test.py          # Script to run an offline test of the deep analysis phase.
│   │   ├── test3_input.xml      # Sample XML input for Phase 3 tests.
│   │   └── test_phase3_offline.py # Offline unit test for the deep analysis phase.
│   ├── phase_4_test/            # Tests for the synthesis phase.
│   │   ├── __init__.py          # Test package initializer.
│   │   ├── output/              # Directory for phase 4 test outputs.
│   │   ├── run_test.py          # Script to run an offline test of the synthesis phase.
│   │   └── test_phase4_offline.py # Offline unit test for the synthesis phase.
│   ├── phase_5_test/            # Tests for the consolidation phase.
│   │   ├── __init__.py          # Test package initializer.
│   │   ├── output/              # Directory for phase 5 test outputs.
│   │   ├── run_test.py          # Script to run an offline test of the consolidation phase.
│   │   └── test_phase5_offline.py # Offline unit test for the consolidation phase.
│   ├── test_cli_services.py     # Unit tests for CLI services and context helpers.
│   ├── test_env.py              # Script to check if required environment variables (API keys) are set.
│   ├── test_openai_responses.py # Unit tests for OpenAI Responses API integration.
│   ├── test_smoke_discovery.py  # A simple placeholder smoke test.
│   ├── tests_input/             # Input files for running tests.
│   │   ├── index.html           # Sample HTML file for testing.
│   │   ├── main.py              # Sample Python/Flask file for testing.
│   │   └── requirements.txt     # Sample requirements file for testing.
│   └── unit/                    # Contains all unit tests.
│       ├── __init__.py          # Unit tests package initializer.
│       ├── agents/              # Unit tests for agent implementations.
│       │   ├── __init__.py      # Agent unit tests package initializer.
│       │   ├── test_anthropic_agent_parsing.py # Tests parsing of Anthropic agent responses.
│       │   ├── test_anthropic_request_builder.py # Tests construction of Anthropic API requests.
│       │   ├── test_deepseek_agent_parsing.py # Tests parsing of DeepSeek agent responses.
│       │   ├── test_deepseek_helpers.py # Tests helpers for the DeepSeek agent implementation.
│       │   ├── test_gemini_agent_parsing.py # Tests parsing of Gemini agent responses.
│       │   ├── test_openai_agent_parsing.py # Tests parsing of OpenAI agent responses.
│       │   └── test_openai_helpers.py # Tests helpers for the OpenAI agent implementation.
│       ├── test_agent_parser_basic.py # Basic unit tests for the agent parser utility.
│       ├── test_agents_anthropic_parse.py # More unit tests for Anthropic agent response parsing.
│       ├── test_agents_deepseek.py # Unit tests for the DeepSeek agent architect.
│       ├── test_agents_gemini_error.py # Tests error handling in the Gemini agent implementation.
│       ├── test_agents_openai_params.py # Tests parameter construction for OpenAI API requests.
│       ├── test_cli.py          # Unit tests for the main CLI application.
│       ├── test_config_service.py # Unit tests for the configuration service.
│       ├── test_dependency_scanner.py # Unit tests for the dependency scanner utility.
│       ├── test_file_retriever.py # Unit tests for the file retriever utility.
│       ├── test_model_config_helper.py # Unit tests for the model config helper.
│       ├── test_model_overrides.py # Tests applying model configuration overrides.
│       ├── test_phase_events.py # Tests the emission of analysis phase events.
│       ├── test_phases_edges.py # Edge case tests for analysis phase logic.
│       ├── test_streaming_support.py # Unit tests for streaming API response handling.
│       ├── test_tavily_tool.py  # Unit tests for the Tavily search tool.
│       └── test_tool_manager.py # Unit tests for the tool manager utility.
└── typings/                     # Type stub files for external libraries.
    └── tavily/                  # Type stubs for the `tavily-python` library.
        └── __init__.pyi         # Type stub file for the tavily client.