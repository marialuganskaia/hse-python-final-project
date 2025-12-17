from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ....domain.models import Event
from ....use_cases.ports import EventRepository
from ..models import EventORM
from ..repositories_base import SQLAlchemyRepository
from .mappers import to_dataclass, to_utc_naive


class EventRepo(SQLAlchemyRepository, EventRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_hackathon(self, hackathon_id: int) -> list[Event]:
        stmt = (
            select(EventORM)
            .where(EventORM.hackathon_id == hackathon_id)
            .order_by(EventORM.starts_at)
        )
        items = (await self.session.execute(stmt)).scalars().all()
        return [to_dataclass(Event, o.__dict__) for o in items]

    async def get_upcoming_events(self, hackathon_id: int, hours_ahead: int) -> list[Event]:
        now = datetime.now(UTC).replace(tzinfo=None)
        upper = now + timedelta(hours=hours_ahead)
        stmt = (
            select(EventORM)
            .where(
                and_(
                    EventORM.hackathon_id == hackathon_id,
                    EventORM.starts_at >= now,
                    EventORM.starts_at <= upper,
                )
            )
            .order_by(EventORM.starts_at)
        )
        items = (await self.session.execute(stmt)).scalars().all()
        return [to_dataclass(Event, o.__dict__) for o in items]

    async def save_all(self, events: list[Event]) -> list[Event]:
        saved_events = []
        for event in events:
            orm_obj = EventORM(
                hackathon_id=event.hackathon_id,
                title=event.title,
                type=event.type,
                starts_at=to_utc_naive(event.starts_at),
                ends_at=to_utc_naive(event.ends_at),
                location=event.location,
                description=event.description,
            )
            self.session.add(orm_obj)
            await self.session.flush()
            saved_events.append(to_dataclass(Event, orm_obj.__dict__))
        await self.session.commit()
        return saved_events
