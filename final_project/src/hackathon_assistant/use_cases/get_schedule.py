from dataclasses import dataclass

from .dto import ScheduleItemDTO
from .ports import EventRepository, UserRepository


@dataclass
class GetScheduleUseCase:
    user_repo: UserRepository
    event_repo: EventRepository

    async def execute(self, telegram_id: int) -> list[ScheduleItemDTO]:
        """Получить расписание текущего хакатона пользователя
        На вход: telegram_id: ID пользователя в tg
        Возвращаем List[ScheduleItemDTO]: список eventов, отсортированный по времени начала
        """
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if user is None or user.current_hackathon_id is None:
            return []

        events = await self.event_repo.get_by_hackathon(user.current_hackathon_id)
        events_sorted = sorted(events, key=lambda e: e.starts_at)

        return [
            ScheduleItemDTO(
                title=e.title,
                starts_at=e.starts_at,
                ends_at=e.ends_at,
                location=e.location,
                description=e.description,
            )
            for e in events_sorted
        ]
