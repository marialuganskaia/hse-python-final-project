from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from ....use_cases.ports import EventRepository as EventRepositoryProtocol
from ..repositories_base import SQLAlchemyRepository
from ..models import EventORM
from ....domain.models import Event


class EventRepo(SQLAlchemyRepository, EventRepositoryProtocol):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_hackathon(self, hackathon_id: int) -> list[Event]:
        """Получить все события хакатона"""
        raise NotImplementedError

    async def get_upcoming_events(self, hackathon_id: int, hours_ahead: int) -> list[Event]:
        """Получить предстоящие события"""
        raise NotImplementedError
