from __future__ import annotations

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from ....use_cases.ports import SubscriptionRepository as SubscriptionRepositoryProtocol
from ..repositories_base import SQLAlchemyRepository
from ..models import ReminderSubscriptionORM, UserORM
from ....domain.models import ReminderSubscription, User


class SubscriptionRepo(SQLAlchemyRepository, SubscriptionRepositoryProtocol):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_user_subscription(self, user_id: int, hackathon_id: int) -> Optional[ReminderSubscription]:
        """Получить подписку пользователя на хакатон"""
        raise NotImplementedError

    async def get_subscribed_users(self, hackathon_id: int) -> list[User]:
        """Получить подписанных пользователей"""
        raise NotImplementedError

    async def count_subscribed_users(self, hackathon_id: int) -> int:
        """Подсчитать подписанных пользователей"""
        raise NotImplementedError

    async def save(self, subscription: ReminderSubscription) -> ReminderSubscription:
        """Сохранить подписку"""
        raise NotImplementedError
