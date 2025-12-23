import math
from dataclasses import dataclass

from ..domain.models import Event
from .ports import EventRepository


@dataclass
class GetUpcomingEventsUseCase:
    event_repo: EventRepository

    async def execute(self, hackathon_id: int, minutes_ahead: int = 15) -> list[Event]:
        """Получить события, которые начнутся через minutes_ahead минут"""
        hours_ahead = max(1, math.ceil(minutes_ahead / 60))

        return await self.event_repo.get_upcoming_events(
            hackathon_id=hackathon_id,
            hours_ahead=hours_ahead,
        )
