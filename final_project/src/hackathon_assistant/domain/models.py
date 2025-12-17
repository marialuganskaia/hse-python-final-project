from __future__ import annotations

from dataclasses import InitVar, dataclass, field
from datetime import datetime
from enum import Enum, StrEnum
from typing import Any


class UserRole(StrEnum):
    PARTICIPANT = "participant"
    ORGANIZER = "organizer"


class EventType(StrEnum):
    CHECKPOINT = "checkpoint"
    DEADLINE = "deadline"
    MEETUP = "meetup"
    LECTURE = "lecture"
    OTHER = "other"


def _enum_values(enum_cls: type[Enum]) -> str:
    return ", ".join([e.value for e in enum_cls])  # type: ignore[attr-defined]


def _require_non_empty(value: Any, message: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(message)


def _require_positive_int(value: Any, message: str) -> None:
    if not isinstance(value, int) or value <= 0:
        raise ValueError(message)


@dataclass
class User:
    telegram_id: int
    username: str = ""
    first_name: str = ""
    last_name: str = ""
    role: UserRole = UserRole.PARTICIPANT
    current_hackathon_id: int | None = None
    id: int | None = None

    def __post_init__(self) -> None:
        _require_positive_int(self.telegram_id, "telegram_id должен быть положительным числом")

        if not isinstance(self.role, UserRole):
            raise ValueError(f"Роль должна быть одной из: {_enum_values(UserRole)}")

    def is_organizer(self) -> bool:
        return self.role == UserRole.ORGANIZER


@dataclass
class Hackathon:
    code: str
    name: str
    description: str = ""
    start_at: datetime = field(default_factory=datetime.now)
    end_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    id: int | None = None

    def __post_init__(self) -> None:
        _require_non_empty(self.code, "Код хакатона не может быть пустым")
        _require_non_empty(self.name, "Название хакатона не может быть пустым")

        if not isinstance(self.start_at, datetime) or not isinstance(self.end_at, datetime):
            raise ValueError("Дата начала должна быть раньше даты окончания")

        if self.start_at >= self.end_at:
            raise ValueError("Дата начала должна быть раньше даты окончания")


@dataclass
class Event:
    hackathon_id: int
    title: str
    type: EventType = EventType.OTHER
    starts_at: datetime = field(default_factory=datetime.now)
    ends_at: datetime = field(default_factory=datetime.now)
    location: str | None = None
    description: str | None = None
    id: int | None = None

    # aliases for tests / legacy code:
    start_at: InitVar[datetime | None] = None
    end_at: InitVar[datetime | None] = None

    def __post_init__(self, start_at: datetime | None, end_at: datetime | None) -> None:
        _require_positive_int(self.hackathon_id, "ID хакатона должен быть положительным числом")
        _require_non_empty(self.title, "Название события не может быть пустым")

        if not isinstance(self.type, EventType):
            raise ValueError(f"Тип события должен быть одним из: {_enum_values(EventType)}")

        # apply aliases if provided
        if start_at is not None:
            self.starts_at = start_at
        if end_at is not None:
            self.ends_at = end_at

        if not isinstance(self.starts_at, datetime) or not isinstance(self.ends_at, datetime):
            raise ValueError("Начало события должно быть раньше окончания")

        if self.starts_at >= self.ends_at:
            raise ValueError("Начало события должно быть раньше окончания")


@dataclass
class FAQItem:
    hackathon_id: int
    question: str
    answer: str
    id: int | None = None

    def __post_init__(self) -> None:
        _require_positive_int(self.hackathon_id, "ID хакатона должен быть положительным числом")
        _require_non_empty(self.question, "Вопрос не может быть пустым")
        _require_non_empty(self.answer, "Ответ не может быть пустым")


@dataclass
class Rules:
    hackathon_id: int
    content: str
    id: int | None = None

    def __post_init__(self) -> None:
        _require_positive_int(self.hackathon_id, "ID хакатона должен быть положительным числом")
        _require_non_empty(self.content, "Текст правил не может быть пустым")


@dataclass
class ReminderSubscription:
    user_id: int
    hackathon_id: int
    enabled: bool = True
    id: int | None = None

    def __post_init__(self) -> None:
        _require_positive_int(self.user_id, "ID пользователя должен быть положительным числом")
        _require_positive_int(self.hackathon_id, "ID хакатона должен быть положительным числом")
