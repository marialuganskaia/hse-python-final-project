from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ....domain.models import Rules
from ....use_cases.ports import RulesRepository
from ..models import RulesORM
from ..repositories_base import SQLAlchemyRepository
from .mappers import to_dataclass


class RulesRepo(SQLAlchemyRepository, RulesRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_for_hackathon(self, hackathon_id: int) -> Rules | None:
        stmt = select(RulesORM).where(RulesORM.hackathon_id == hackathon_id)
        orm_obj = (await self.session.execute(stmt)).scalars().first()
        return None if orm_obj is None else to_dataclass(Rules, orm_obj.__dict__)

    async def save(self, rules: Rules) -> Rules:
        stmt = select(RulesORM).where(RulesORM.hackathon_id == rules.hackathon_id)
        result = await self.session.execute(stmt)
        orm_obj = result.scalar_one_or_none()

        if orm_obj is None:
            orm_obj = RulesORM(
                hackathon_id=rules.hackathon_id,
                content=rules.content,
            )
            self.session.add(orm_obj)
        else:
            orm_obj.content = rules.content

        await self.session.commit()
        await self.session.refresh(orm_obj)
        return to_dataclass(Rules, orm_obj.__dict__)
