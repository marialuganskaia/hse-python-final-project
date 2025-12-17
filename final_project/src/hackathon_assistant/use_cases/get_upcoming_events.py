from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List
from .dto import EventDTO
from .ports import EventRepository
from ..domain.models import Event


@dataclass
class GetUpcomingEventsUseCase:
    event_repo: EventRepository
    
    async def execute(self, hackathon_id: int, minutes_ahead: int = 15) -> List[Event]:
        """Получить события, которые начнутся через minutes_ahead минут"""
        # TODO: Реализовать, когда EventRepository будет готов
        # Временная заглушка для тестирования
        
        # Создаем тестовое событие как доменную модель
        return [
            Event(
                id=1,
                hackathon_id=hackathon_id,
                title="Тестовое событие",
                description="Описание тестового события для демонстрации",
                starts_at=datetime.now() + timedelta(minutes=20),
                ends_at=datetime.now() + timedelta(hours=1),
                location="Аудитория 101",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]
