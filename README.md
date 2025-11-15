# sky-mood

daily text sent to report the forecast in a playful poem

## Prerequisites

- Node.js 22.12+ (or 20.19 LTS) for the Vite frontend.
- Python 3.12 for the FastAPI backend.
- npm and python3 available on your PATH.

## Initial setup

```bash
# install frontend deps
cd web && npm install

# set up backend virtualenv + deps
cd ../api
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Development workflow

Use the repo-level CLI to run both services with hot reload:

```bash
./c dev
```

This launches:

- Vite dev server on http://localhost:5173
- FastAPI (uvicorn --reload) on http://localhost:8000

Stop both processes with `Ctrl+C`.

## Project layout

- `web/` – React frontend (Vite)
- `api/` – FastAPI backend
- `c` / `tools/cli.py` – helper CLI commands
