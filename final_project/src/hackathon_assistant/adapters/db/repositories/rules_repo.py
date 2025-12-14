from __future__ import annotations

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from ....use_cases.ports import RulesRepository as RulesRepositoryProtocol
from ..repositories_base import SQLAlchemyRepository
from ..models import RulesORM
from ....domain.models import Rules


class RulesRepo(SQLAlchemyRepository, RulesRepositoryProtocol):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_for_hackathon(self, hackathon_id: int) -> Optional[Rules]:
        """Получить правила хакатона"""
        raise NotImplementedError