.
├── __init__.py                # Exports the main Typer application object.
├── app.py                     # Defines the main Typer CLI application and registers subcommands.
├── bootstrap.py               # Handles common CLI runtime initialization like logging and config.
├── commands/                  # Contains implementations for CLI subcommands.
│   ├── __init__.py            # Marks the 'commands' directory as a Python package.
│   ├── analyze.py             # Implements the 'analyze' subcommand to run the analysis pipeline.
│   ├── configure.py           # Implements the 'configure' subcommand for various settings.
│   └── keys.py                # Implements the 'keys' subcommand to display provider API keys.
├── context.py                 # Defines the shared CLI context and helper functions.
├── services/                  # Contains business logic and abstractions for CLI commands.
│   ├── __init__.py            # Marks the 'services' directory as a Python package.
│   ├── configuration.py       # Service layer for managing application configuration.
│   └── pipeline_runner.py     # Logic for executing the core analysis pipeline.
└── ui/                        # Contains user interface components and interactive flows.
    ├── __init__.py            # Marks the 'ui' directory as a Python package.
    ├── analysis_view.py       # Rich-based view for displaying analysis progress.
    ├── main_menu.py           # Implements the interactive main menu for the CLI.
    ├── settings/              # Contains interactive flows for managing settings.
    │   ├── __init__.py        # Exports settings configuration functions.
    │   ├── exclusions/        # UI flows for managing file and directory exclusion rules.
    │   │   ├── __init__.py    # Main entry point for the interactive exclusion settings UI.
    │   │   ├── editor.py      # Prompts for adding or editing exclusion values.
    │   │   └── summary.py     # Renders a summary table of current exclusion rules.
    │   ├── logging.py         # Interactive flow for configuring logging verbosity.
    │   ├── menu.py            # The main interactive settings menu.
    │   ├── models/            # UI flows for configuring model presets.
    │   │   ├── __init__.py    # Main entry point for the model preset configuration UI.
    │   │   ├── researcher.py  # Specific UI for configuring the researcher agent.
    │   │   └── utils.py       # Helper functions for building model selection prompts.
    │   ├── outputs.py         # Interactive flow for configuring output generation preferences.
    │   └── providers.py       # Interactive flow for managing provider API keys.
    └── styles.py              # Defines shared styles and helpers for Questionary prompts.