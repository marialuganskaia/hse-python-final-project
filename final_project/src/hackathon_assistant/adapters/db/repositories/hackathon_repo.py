from __future__ import annotations

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from ....use_cases.ports import HackathonRepository as HackathonRepositoryProtocol
from ..repositories_base import SQLAlchemyRepository
from ..models import HackathonORM
from ....domain.models import Hackathon


class HackathonRepo(SQLAlchemyRepository, HackathonRepositoryProtocol):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_code(self, code: str) -> Optional[Hackathon]:
        """Найти хакатон по коду"""
        raise NotImplementedError

    async def get_all_active(self) -> list[Hackathon]:
        """Получить все активные хакатоны"""
        raise NotImplementedError
