from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    bot_token: str
    database_url: str

    allowed_admin_ids: list[int] = []

    @field_validator("allowed_admin_ids", mode="before")
    @classmethod
    def _parse_allowed_admin_ids(cls, v: Any) -> list[int]:
        if v is None or v == "":
            return []
        if isinstance(v, list):
            return [int(x) for x in v]
        if isinstance(v, str):
            s = v.strip()
            # JSON
            if s.startswith("[") and s.endswith("]"):
                data = json.loads(s)
                return [int(x) for x in data]
            # CSV
            return [int(x.strip()) for x in s.split(",") if x.strip()]
        return [int(v)]

    reminders_enabled: bool = True
    reminder_interval_minutes: int = 5

    model_config = SettingsConfigDict(
        env_file=_PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
