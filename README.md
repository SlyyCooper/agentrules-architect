# 🤖 AgentRules Architect v3

<div align="center">

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![OpenAI](https://img.shields.io/badge/OpenAI-o3%20%7C%20o4--mini%20%7C%20gpt--5-blue.svg)](https://openai.com/)
[![Anthropic](https://img.shields.io/badge/Anthropic-claude--4.5%20family-purple.svg)](https://www.anthropic.com/)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-reasoner-red.svg)](https://deepseek.com/)
[![Google](https://img.shields.io/badge/Google-gemini--2.5--flash%20%7C%20gemini--2.5--pro-green.svg)](https://ai.google.dev/)
[![xAI](https://img.shields.io/badge/xAI-grok--4--family-black.svg)](https://x.ai/)
[![Built By](https://img.shields.io/badge/Built%20By-SlyyCooper-orange.svg)](https://github.com/SlyyCooper)

**Your multi-provider AI code analysis and AGENTS.md generator 🚀**

[Highlights](#-v3-highlights) • [Features](#-feature-overview) • [Requirements](#-requirements) • [Installation](#-installation) • [CLI](#-cli-at-a-glance) • [Configuration](#-configuration--preferences) • [Architecture](#-project-architecture) • [Outputs](#-output-artifacts) • [Development](#-development-workflow)

</div>

## Why AgentRules Architect?

Version 3 rebrands the project from **CursorRules Architect** to **AgentRules Architect** to match the standardized `AGENTS.md` contract used across modern AI coding agents. The rename comes with a fresh Typer-powered CLI, a persistent configuration service, broader provider support (including xAI Grok and OpenAI GPT‑5 presets), and a tooling layer that keeps the six-phase analysis pipeline predictable, auditable, and ready for enterprise use.

## 🔥 v3 Highlights

- ✨ **Rebrand & packaging** – published as the `agentrules` Python package with a slim `main.py` entrypoint.
- 🧭 **Typer CLI overhaul** – `agentrules` launches an interactive main menu with subcommands for `analyze`, `configure`, and `keys`.
- 🗂️ **Persistent settings** – API keys, model presets, logging, and output preferences live in `~/.config/agentrules/config.toml` (override with `AGENTRULES_CONFIG_DIR`).
- 🧠 **Expanded provider matrix** – presets now cover Anthropic Claude 4.5, OpenAI o3/o4/GPT‑4.1/GPT‑5, Google Gemini 2.5, DeepSeek Reasoner & Chat, and xAI Grok 4 tiers.
- 🔌 **Unified tool management** – the new `ToolManager` adapts JSON tool schemas for each provider; Tavily web search is available to researcher agents with one toggle.
- 🧪 **Deterministic offline mode** – `agentrules analyze --offline` (or `OFFLINE=1`) swaps in dummy architects and stubbed Tavily responses for CI and local smoke tests.
- ✅ **Test & quality backbone** – 200+ unit/integration tests, Pyright, Ruff, and offline stubs provide confidence without hitting live APIs.

## ✨ Feature Overview

- 🌐 Multi-provider orchestration with consistent streaming telemetry.
- 🔍 Six-phase pipeline: discovery → planning → deep dives → synthesis → consolidation → final AGENTS.md generation.
- 🧩 Researcher tooling via Tavily search with provider-aware tool translation.
- 📊 Rich terminal UI (Rich) showing per-agent progress, duration, and failures in real time.
- 🪵 Configurable outputs: `AGENTS.md`, `.cursorignore`, and per-phase markdown/json snapshots.
- 🔧 Declarative model presets plus runtime overrides via CLI or TOML.

## 🛠 Requirements

- Python **3.11.9+** (matches Pyright target and packaged metadata).
- API key(s) for at least one provider:
  - Anthropic (`claude-haiku-4.5`, `claude-sonnet-4.5`, `claude-opus-4.1`, …)
  - OpenAI (`o3`, `o4-mini`, `gpt-4.1`, `gpt-5`)
  - DeepSeek (`deepseek-reasoner`, `deepseek-chat`)
  - Google (`gemini-2.5-flash`, `gemini-2.5-pro`)
  - xAI (`grok-4` family)
  - Tavily (optional, enables live web search tooling)
- Core dependencies: `anthropic`, `openai`, `google-genai`, `tavily-python`, `rich`, `typer`, `questionary`, `platformdirs`, `pathspec`, `python-dotenv`, `protobuf`.
- Dev tooling: `pytest`, `pytest-asyncio`, `pytest-mock`, `ruff`, `pyright`.

## 📦 Installation

### Clone & bootstrap

```bash
git clone https://github.com/slyycooper/agentrules-architect.git
cd agentrules-architect
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Need a one-liner? Use the helper script:

```bash
./scripts/bootstrap_env.sh           # set PYTHON_BIN=/abs/path/to/python to override interpreter
```

### Quick smoke test

```bash
agentrules --version
agentrules analyze --offline tests/tests_input
```

If you prefer isolated installs (e.g., CI), the package publishes as `agentrules`:

```bash
pip install agentrules
```

## 🔐 Configure API Keys

Run the interactive configurator to store credentials securely:

```bash
agentrules configure
```

- Keys are saved to `~/.config/agentrules/config.toml` (override with `AGENTRULES_CONFIG_DIR`).
- Values are mirrored into environment variables on the next launch.
- Use `agentrules configure --provider openai` for quick single-key updates.
- Show current status with:

```bash
agentrules keys
```

## 🧭 CLI At A Glance

- `agentrules` – interactive main menu (analyze, configure models/outputs, check keys).
- `agentrules analyze /path/to/project` – full six-phase analysis.
  - `--offline` switches to deterministic dummy providers (also enabled via `OFFLINE=1`).
- `agentrules configure --models` – assign presets per phase with guided prompts; the Phase 1 → Researcher entry lets you toggle the agent (`Auto`, `On`, `Off`).
- `agentrules configure --outputs` – toggle `.cursorignore`, `phases_output/`, and custom rules filename.
- `agentrules configure --logging` – set verbosity (`quiet`, `standard`, `verbose`) or export via `AGENTRULES_LOG_LEVEL`.

## ⚙️ Configuration & Preferences

- **Config file**: `~/.config/agentrules/config.toml`
  - `providers` – API keys per provider.
  - `models` – preset IDs applied to each phase (`phase1`, `phase2`, `final`, `researcher`, …).
  - `outputs` – `generate_cursorignore`, `generate_phase_outputs`, `rules_filename`.
  - `features` – `researcher_mode` (`auto`/`on`/`off`) to control Phase 1 web research (managed from the Researcher row in the models wizard).
  - `exclusions` – add/remove directories, files, or extensions; choose to respect `.gitignore`.
- **Runtime helpers** (from `agentrules/config_service.py`):
  - `get_effective_exclusions()` resolves overrides with defaults from `config/exclusions.py`.
  - `should_generate_phase_outputs()` and friends toggle output writers in `core/utils/file_creation`.
- **Environment variables**:
  - `AGENTRULES_CONFIG_DIR` – alternate config root.
  - `AGENTRULES_LOG_LEVEL` – overrides persisted verbosity.
  - `AGENTRULES_RULES_FILENAME` (alias of `DEFAULT_RULES_FILENAME`) – customize the generated `AGENTS.md` name.

## 🧠 Model Presets & Providers

Presets live in `config/agents.py` via the `MODEL_PRESETS` dictionary. Each preset bundles:

- Provider (`ModelProvider`)
- Model name plus reasoning/temperature configuration
- Human-readable label and description for the CLI wizard

Defaults favor `gemini-2.5-flash` for every phase, but you can mix providers:

```python
MODEL_PRESET_DEFAULTS = {
    "phase1": "gemini-flash",
    "phase2": "claude-sonnet-reasoning",
    "phase3": "o3-high",
    "phase4": "deepseek-reasoner",
    "phase5": "grok-4-fast-reasoning",
    "final": "gpt5-high",
    "researcher": "gemini-pro",
}
```

Adjust presets through the CLI (`agentrules configure --models`) or by editing `config/agents.py`. At runtime the values populate `MODEL_CONFIG`, which the pipeline reads in `agentrules/analyzer.py`.

## 🔍 Tooling & Research Agents

- `core/agent_tools/tool_manager.py` normalizes JSON tool schemas for each provider.
- `config/tools.py` exposes `TOOL_SETS` and a `with_tools_enabled` helper for models that accept function/tool calls.
- Tavily search (`tavily_web_search`) ships as the default researcher tool. Set `TAVILY_API_KEY` and leave the researcher mode on `Auto` so Phase 1 opts in automatically; switch to `On` or `Off` from the models wizard’s Researcher entry. When disabled (or no key is present), documentation research is skipped; offline runs force the researcher on for smoke coverage. The dependency agent automatically downgrades from “knowledge gaps” mode to its legacy full catalog so downstream agents still receive usable dependency data when research is unavailable.

## 🧱 Project Architecture

- `agentrules/` – Typer CLI, interactive Questionary flows, Rich UI, configuration services, and pipeline runner (`agentrules/SNAPSHOT.md`).
- `core/` – provider-specific architects (`core/agents`), analysis phases (`core/analysis`), tool adapters (`core/agent_tools`), streaming primitives, and filesystem utilities (`core/SNAPSHOT.md`).
- `config/` – preset definitions, exclusions, prompts, and tool bindings (`config/SNAPSHOT.md`).
- `tests/` – live/offline smoke tests, phase-specific suites, provider fixtures, and unit coverage for helpers and stubs.
- `main.py` – minimalist entrypoint that exposes the Typer app.
- `pyproject.toml` – package metadata, scripts, Ruff/Pyright config, and dependency declarations.

## 🧾 Output Artifacts

By default the pipeline produces:

- `AGENTS.md` (or your custom rules filename) – cleaned, standardized agent instructions.
- `.cursorignore` – generated when enabled to keep editor agents focused on relevant files.
- `phases_output/` – per-phase markdown/JSON snapshots for auditing and downstream automation.
- Rich console logs summarizing model usage, timing, and file counts.

Toggle outputs with `agentrules configure --outputs` or via the config TOML.

## 🛠 Development Workflow

- Install dev extras: `pip install -e .[dev]`
- Format & lint: `ruff format . && ruff check .`
- Static typing: `pyright`
- Run targeted tests: `python tests/phase_3_test/run_test.py`
- Full suite: `python -m unittest discover tests -v`
- Keep docs and presets in sync when adding providers (`config/agents.py`, `config/tools.py`, `core/agents/*`).

## 🤝 Contributing

See `CONTRIBUTING.md` for detailed guidelines on workflows, testing, and pull request expectations. Issues and PRs are welcome—just ensure Ruff/Pyright/tests pass before submitting.

## 📄 License

Released under the MIT License. See `LICENSE` for details.
