from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ScheduleItemDTO:
    """DTO для элемента расписания"""
    title: str
    starts_at: datetime
    ends_at: datetime
    location: Optional[str] = None
    description: Optional[str] = None


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
    description: Optional[str] = None
    location: Optional[str] = None
    code: Optional[str] = None


@dataclass
class BroadcastResultDTO:
    """DTO для результата рассылки"""
    total_recipients: int
    sent_successfully: int
    failed: int
    success_rate: float
