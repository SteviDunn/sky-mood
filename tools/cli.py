from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path

import click

ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = ROOT / "web"
API_DIR = ROOT / "api"
API_VENV = API_DIR / ".venv"
PYTHON_BIN = API_VENV / "bin" / "python"


@click.group()
def cli() -> None:
    """Utility commands for developing Sky Mood."""


@cli.command()
@click.option("--frontend-port", default=5173, show_default=True, help="Port for Vite dev server")
@click.option("--backend-port", default=8000, show_default=True, help="Port for FastAPI server")
def dev(frontend_port: int, backend_port: int) -> None:
    """Run frontend and backend dev servers concurrently."""

    _validate_environment()

    commands = [
        {
            "name": "frontend",
            "cmd": [
                "npm",
                "run",
                "dev",
                "--",
                "--host",
                "0.0.0.0",
                "--port",
                str(frontend_port),
            ],
            "cwd": WEB_DIR,
            "env": os.environ.copy(),
        },
        {
            "name": "backend",
            "cmd": [
                str(PYTHON_BIN),
                "-m",
                "uvicorn",
                "app.main:app",
                "--reload",
                "--host",
                "0.0.0.0",
                "--port",
                str(backend_port),
            ],
            "cwd": API_DIR,
            "env": _with_python_path(os.environ.copy(), API_DIR),
        },
    ]

    processes: list[tuple[str, subprocess.Popen[bytes]]] = []
    try:
        for entry in commands:
            click.echo(f"Starting {entry['name']} -> {' '.join(entry['cmd'])} (cwd={entry['cwd']})")
            proc = subprocess.Popen(
                entry["cmd"],
                cwd=str(entry["cwd"]),
                env=entry["env"],
            )
            processes.append((entry["name"], proc))

        _monitor_processes(processes)
    except KeyboardInterrupt:
        click.echo("Received Ctrl+C, shutting down...")
    finally:
        _terminate_processes(processes)


def _monitor_processes(processes: list[tuple[str, subprocess.Popen[bytes]]]) -> None:
    while processes:
        for name, proc in list(processes):
            exit_code = proc.poll()
            if exit_code is not None:
                raise click.ClickException(f"{name} exited with code {exit_code}")
        time.sleep(0.5)


def _terminate_processes(processes: list[tuple[str, subprocess.Popen[bytes]]]) -> None:
    for name, proc in processes:
        if proc.poll() is None:
            click.echo(f"Stopping {name}...")
            proc.terminate()
    for _, proc in processes:
        if proc.poll() is None:
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()


def _validate_environment() -> None:
    if not WEB_DIR.exists():
        raise click.ClickException("Missing web directory. Did you scaffold the frontend?")
    if not API_DIR.exists():
        raise click.ClickException("Missing api directory. Did you scaffold the backend?")
    if not PYTHON_BIN.exists():
        raise click.ClickException(
            "FastAPI virtualenv not found. Run 'python3 -m venv api/.venv && '\n"
            "'.venv/bin/pip install -r api/requirements.txt' before using 'dev'."
        )


def _with_python_path(env: dict[str, str], additional_path: Path) -> dict[str, str]:
    current = env.get("PYTHONPATH", "")
    extra = str(additional_path)
    env["PYTHONPATH"] = f"{extra}:{current}" if current else extra
    return env


if __name__ == "__main__":
    cli()
