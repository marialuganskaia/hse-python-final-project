from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from ....use_cases.ports import FAQRepository as FAQRepositoryProtocol
from ..repositories_base import SQLAlchemyRepository
from ..models import FAQItemORM
from ....domain.models import FAQItem


class FAQRepo(SQLAlchemyRepository, FAQRepositoryProtocol):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_hackathon(self, hackathon_id: int) -> list[FAQItem]:
        """Получить все FAQ хакатона"""
        raise NotImplementedError
