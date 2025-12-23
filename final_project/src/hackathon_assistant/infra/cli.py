from __future__ import annotations

import argparse
import asyncio
import json
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from hackathon_assistant.domain.models import EventType
from hackathon_assistant.infra.db import db_ping, get_session
from hackathon_assistant.infra.repositories import RepositoryProvider
from hackathon_assistant.infra.settings import get_settings
from hackathon_assistant.use_cases.create_hackathon import CreateHackathonFromConfigUseCase


def _parse_dt(value: Any, field_name: str) -> datetime:
    if isinstance(value, datetime):
        return value
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be ISO datetime string")
    v = value.replace("Z", "+00:00")
    return datetime.fromisoformat(v)


def _normalize_config(data: dict[str, Any]) -> dict[str, Any]:
    """
    Поддерживаем два формата:
    1) { "hackathon": {...}, "events": [...], "rules": {...}, "faq": [...] }
    2) плоский { "name": ..., "code": ..., "events": ..., "rules": ..., "faq": ... }
    """
    if isinstance(data.get("hackathon"), dict):
        config: dict[str, Any] = dict(data["hackathon"])
        config["events"] = data.get("events", [])
        config["rules"] = data.get("rules")
        config["faq"] = data.get("faq", [])
    else:
        config = dict(data)

    # hackathon даты
    config["start_at"] = _parse_dt(config.get("start_at"), "start_at")
    config["end_at"] = _parse_dt(config.get("end_at"), "end_at")

    # events: даты + enum
    events = config.get("events") or []
    if not isinstance(events, list):
        raise ValueError("events must be a list")
    for e in events:
        if not isinstance(e, dict):
            raise ValueError("each event must be an object")
        if "starts_at" in e:
            e["starts_at"] = _parse_dt(e["starts_at"], "events[].starts_at")
        if "ends_at" in e:
            e["ends_at"] = _parse_dt(e["ends_at"], "events[].ends_at")
        if "type" in e:
            t = e["type"]
            if isinstance(t, EventType):
                continue
            if isinstance(t, str):
                try:
                    e["type"] = EventType(t)
                except ValueError:
                    e["type"] = EventType[t.upper()]
            else:
                raise ValueError("events[].type must be string or EventType")
    config["events"] = events

    return config


@dataclass(frozen=True)
class CLI:
    def build_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            prog="hackathon-assistant",
            description="Hackathon Assistant CLI",
        )
        sub = parser.add_subparsers(dest="command", required=True)

        ping = sub.add_parser("db-ping", help="Check DB connectivity")
        ping.set_defaults(_handler=self._cmd_db_ping)

        create = sub.add_parser("create-hackathon", help="Create hackathon from JSON config")
        create.add_argument("--config", type=Path, required=True, help="Path to JSON config file")
        create.set_defaults(_handler=self._cmd_create_hackathon)

        return parser

    def run(self, argv: Sequence[str] | None = None) -> int:
        parser = self.build_parser()
        args = parser.parse_args(list(argv) if argv is not None else None)
        handler = getattr(args, "_handler", None)
        if handler is None:
            parser.error("No command handler")
        return asyncio.run(handler(args))

    async def _cmd_db_ping(self, _: argparse.Namespace) -> int:
        settings = get_settings()
        print(f"DATABASE_URL={settings.database_url}")
        ok = await db_ping()
        print("DB ping OK" if ok else "DB ping failed")
        return 0 if ok else 2

    async def _cmd_create_hackathon(self, args: argparse.Namespace) -> int:
        config_path: Path = args.config
        if not config_path.exists():
            print(f"Config not found: {config_path}")
            return 2
        if config_path.suffix.lower() != ".json":
            print("Only JSON config is supported for now.")
            return 2

        raw: dict[str, Any] = json.loads(config_path.read_text(encoding="utf-8"))
        config = _normalize_config(raw)

        async with get_session() as session:
            repos = RepositoryProvider(session=session)

            existing = await repos.hackathon_repo().get_by_code(config["code"])
            if existing is not None:
                print(
                    f"Hackathon already exists: id={existing.id} code={existing.code!r} "
                    f"name={existing.name!r}"
                )
                print("If you want to create a new one, change `code` in the config JSON.")
                return 0

            use_case = CreateHackathonFromConfigUseCase(
                hackathon_repo=repos.hackathon_repo(),
                event_repo=repos.event_repo(),
                faq_repo=repos.faq_repo(),
                rules_repo=repos.rules_repo(),
            )
            result = await use_case.execute(config)

        print(f"Created hackathon id={result.id} code={result.code!r} name={result.name!r}")
        return 0


def main(argv: Sequence[str] | None = None) -> int:
    return CLI().run(argv)
