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
