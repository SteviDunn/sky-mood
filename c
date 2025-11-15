#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_PYTHON="$ROOT_DIR/api/.venv/bin/python"

if [[ ! -x "$VENV_PYTHON" ]]; then
  echo "FastAPI virtualenv missing. Run 'python3 -m venv api/.venv && .venv/bin/pip install -r api/requirements.txt'." >&2
  exit 1
fi

exec "$VENV_PYTHON" -m tools.cli "$@"
