from __future__ import annotations

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from ....use_cases.ports import UserRepository
from ..repositories_base import SQLAlchemyRepository
from ..models import UserORM
from ....domain.models import User

class UserRepo(SQLAlchemyRepository, UserRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Найти пользователя по telegram_id (для /start)"""
        raise NotImplementedError

    async def save(self, user: User) -> User:
        """Сохранить нового пользователя (регистрация в /start)"""
        raise NotImplementedError

    async def update_current_hackathon(self, user_id: int, hackathon_id: int) -> None:
        """Обновить текущий хакатон пользователя (/hackathon)"""
        raise NotImplementedError

    async def count_all(self) -> int:
        """Подсчитать всех пользователей (/admin_stats)"""
        raise NotImplementedError

    async def count_by_hackathon(self, hackathon_id: int) -> int:
        """Подсчитать пользователей по хакатону (/admin_stats)"""
        raise NotImplementedError
