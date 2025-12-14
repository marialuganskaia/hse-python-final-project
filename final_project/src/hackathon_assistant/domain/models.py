from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """Роли пользователей"""

    PARTICIPANT = "participant"
    ORGANIZER = "organizer"


class EventType(str, Enum):
    """Типы событий (предварительно)"""

    CHECKPOINT = "checkpoint"
    DEADLINE = "deadline"
    MEETUP = "meetup"
    LECTURE = "lecture"
    OTHER = "other"


@dataclass
class User:
    """Участник или организатор хакатона"""

    telegram_id: int
    id: int | None = None
    username: str = ""
    first_name: str = ""
    last_name: str = ""
    role: UserRole = UserRole.PARTICIPANT
    current_hackathon_id: int | None = None  # Внешний ключ Hackathon.id

    def is_organizer(self) -> bool:
        """Проверяет, организатор ли пользователь"""
        return self.role == UserRole.ORGANIZER


@dataclass
class Hackathon:
    """Хакатон"""

    code: str
    name: str
    end_at: datetime
    description: str = ""
    start_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True


@dataclass
class Event:
    """Событие в расписании хакатона"""

    hackathon_id: int  # Внешний ключ на Hackathon.id
    title: str
    ends_at: datetime
    id: int | None = None
    type: EventType = EventType.OTHER
    starts_at: datetime = field(default_factory=datetime.now)
    location: str | None = None
    description: str | None = None


@dataclass
class FAQItem:
    """Вопрос-ответ для хакатона"""

    hackathon_id: int  # Внешний ключ на Hackathon.id
    question: str
    answer: str
    id: int | None = None


@dataclass
class Rules:
    """Правила и критерии оценки хакатона"""

    hackathon_id: int  # Внешний ключ на Hackathon.id
    content: str
    id: int | None = None


@dataclass
class ReminderSubscription:
    """Подписка на напоминания о событиях"""

    user_id: int  # Внешний ключ на User.id
    hackathon_id: int  # Внешний ключ на Hackathon.id
    id: int | None = None
    enabled: bool = True
