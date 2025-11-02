#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_NAME=".venv"
ENV_PATH="${PROJECT_ROOT}/${ENV_NAME}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

echo "[bootstrap] project root: ${PROJECT_ROOT}"
echo "[bootstrap] virtualenv target: ${ENV_PATH}"

if [[ ! -d "${ENV_PATH}" ]]; then
  echo "[bootstrap] creating virtual environment with ${PYTHON_BIN} -m venv ${ENV_NAME}"
  "${PYTHON_BIN}" -m venv "${ENV_PATH}"
else
  echo "[bootstrap] virtual environment already exists; skipping creation"
fi

source "${ENV_PATH}/bin/activate"

echo "[bootstrap] upgrading packaging tooling"
pip install --upgrade pip setuptools wheel > /tmp/agentrules_bootstrap_pip.log

echo "[bootstrap] installing project in editable mode with dev extras"
pip install -e '.[dev]' > /tmp/agentrules_bootstrap_install.log

RUN_CHECKS="yes"
if [[ "${1:-}" == "--skip-checks" ]]; then
  RUN_CHECKS="no"
fi

if [[ "${RUN_CHECKS}" == "yes" ]]; then
  echo "[bootstrap] running ruff check"
  ruff check "${PROJECT_ROOT}"
  echo "[bootstrap] running pyright"
  pyright
else
  echo "[bootstrap] skipping ruff/pyright checks"
fi

echo "[bootstrap] done"
