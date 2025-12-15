from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ....domain.models import FAQItem
from ....use_cases.ports import FAQRepository
from ..models import FAQItemORM
from ..repositories_base import SQLAlchemyRepository
from .mappers import to_dataclass


class FAQRepo(SQLAlchemyRepository, FAQRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_hackathon(self, hackathon_id: int) -> list[FAQItem]:
        stmt = (
            select(FAQItemORM)
            .where(FAQItemORM.hackathon_id == hackathon_id)
            .order_by(FAQItemORM.id)
        )
        items = (await self.session.execute(stmt)).scalars().all()
        return [to_dataclass(FAQItem, o.__dict__) for o in items]
