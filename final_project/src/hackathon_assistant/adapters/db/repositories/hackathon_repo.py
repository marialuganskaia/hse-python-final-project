from __future__ import annotations

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ....domain.models import Hackathon
from ....use_cases.ports import HackathonRepository
from ..models import HackathonORM
from ..repositories_base import SQLAlchemyRepository
from .mappers import to_dataclass, to_utc_naive


class HackathonRepo(SQLAlchemyRepository, HackathonRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_code(self, code: str) -> Hackathon | None:
        stmt = select(HackathonORM).where(HackathonORM.code == code)
        orm_obj = (await self.session.execute(stmt)).scalars().first()
        return None if orm_obj is None else to_dataclass(Hackathon, orm_obj.__dict__)

    async def get_all_active(self) -> list[Hackathon]:
        stmt = select(HackathonORM).where(HackathonORM.is_active == True)  # noqa: E712
        items = (await self.session.execute(stmt)).scalars().all()
        return [to_dataclass(Hackathon, o.__dict__) for o in items]

    async def get_by_id(self, hackathon_id: int) -> Hackathon | None:
        stmt = select(HackathonORM).where(HackathonORM.id == hackathon_id)
        orm_obj = (await self.session.execute(stmt)).scalars().first()
        return None if orm_obj is None else to_dataclass(Hackathon, orm_obj.__dict__)

    async def save(self, hackathon: Hackathon) -> Hackathon:
        data = {k: v for k, v in hackathon.__dict__.items() if hasattr(HackathonORM, k)}
        data["start_at"] = to_utc_naive(data.get("start_at"))
        data["end_at"] = to_utc_naive(data.get("end_at"))

        if getattr(hackathon, "id", None) is None:
            orm_obj = HackathonORM(**data)
            self.session.add(orm_obj)
            await self.session.commit()
            await self.session.refresh(orm_obj)
            return to_dataclass(Hackathon, orm_obj.__dict__)

        stmt = update(HackathonORM).where(HackathonORM.id == hackathon.id).values(**data)
        await self.session.execute(stmt)
        await self.session.commit()
        return hackathon
