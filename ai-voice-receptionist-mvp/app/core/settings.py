from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"


def _load_env_file(path: Path = ENV_PATH) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line.removeprefix("export ").strip()
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


_load_env_file()


def _get_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class AppSettings:
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", "8000"))
    app_module: str = os.getenv("APP_MODULE", "app.main:app")
    python: str = os.getenv("PYTHON", "python3")
    venv_dir: str = os.getenv("VENV_DIR", ".venv")
    title: str = os.getenv("APP_TITLE", "AI Voice Receptionist MVP")
    version: str = os.getenv("APP_VERSION", "0.1.0")
    description: str = os.getenv(
        "APP_DESCRIPTION",
        "Lean workflow foundation for missed calls, bookings, FAQ, transfer, and WhatsApp follow-up.",
    )
    environment: str = os.getenv("ENVIRONMENT", "local")
    log_level: str = os.getenv("LOG_LEVEL", "info")
    reload: bool = _get_bool("RELOAD", True)


settings = AppSettings()
