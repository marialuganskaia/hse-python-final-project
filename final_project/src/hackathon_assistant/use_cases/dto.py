from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScheduleItemDTO:
    """DTO для элемента расписания"""

    title: str
    starts_at: datetime
    ends_at: datetime
    location: str | None = None
    description: str | None = None


@dataclass
class RulesDTO:
    """DTO для правил хакатона"""

    content: str


@dataclass
class FAQItemDTO:
    """DTO для FAQ"""

    question: str
    answer: str


@dataclass
class AdminStatsDTO:
    """DTO для статистики администратора"""

    total_users: int
    participants: int
    organizers: int
    subscribed_users: int


@dataclass
class BroadcastTargetDTO:
    """DTO для цели рассылки"""

    user_id: int
    telegram_id: int
    username: str = ""
    first_name: str = ""


@dataclass
class HackathonDTO:
    """DTO для информации о хакатоне"""

    name: str
    start_date: datetime
    end_date: datetime
    description: str | None = None
    location: str | None = None
    code: str | None = None


@dataclass
class BroadcastResultDTO:
    """DTO для результата рассылки"""

    total_recipients: int
    sent_successfully: int
    failed: int
    success_rate: float

@dataclass
class EventDTO:
    id: int
    title: str
    starts_at: datetime
    ends_at: datetime
    location: str | None = None
    description: str | None = None

@dataclass
class ReminderEventDTO:
    """DTO для напоминания об ивенте"""

    event_id: int
    title: str
    starts_at: datetime


@dataclass
class ReminderParticipantDTO:
    """DTO для напоминания об ивенте конкретному челу"""

    user_id: int
    telegram_id: int


@dataclass
class ReminderPileDTO:
    """DTO для напоминания об ивенте сразу пачке людей"""
    event: ReminderEventDTO
    participants: list[ReminderParticipantDTO]
