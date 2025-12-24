from __future__ import annotations

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ....domain.models import ReminderSubscription, User
from ....use_cases.ports import SubscriptionRepository
from ..models import ReminderSubscriptionORM, UserORM
from ..repositories_base import SQLAlchemyRepository
from .mappers import to_dataclass


class SubscriptionRepo(SQLAlchemyRepository, SubscriptionRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_user_subscription(
        self, user_id: int, hackathon_id: int
    ) -> ReminderSubscription | None:
        stmt = select(ReminderSubscriptionORM).where(
            ReminderSubscriptionORM.user_id == user_id,
            ReminderSubscriptionORM.hackathon_id == hackathon_id,
        )
        orm_obj = (await self.session.execute(stmt)).scalars().first()
        return None if orm_obj is None else to_dataclass(ReminderSubscription, orm_obj.__dict__)

    async def save(self, subscription: ReminderSubscription) -> ReminderSubscription:
        if getattr(subscription, "id", None) is None:
            orm_obj = ReminderSubscriptionORM(
                user_id=subscription.user_id,
                hackathon_id=subscription.hackathon_id,
                enabled=subscription.enabled,
            )
            self.session.add(orm_obj)
            await self.session.commit()
            await self.session.refresh(orm_obj)
            return to_dataclass(ReminderSubscription, orm_obj.__dict__)

        stmt = (
            update(ReminderSubscriptionORM)
            .where(ReminderSubscriptionORM.id == subscription.id)
            .values(enabled=subscription.enabled)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        return subscription

    async def get_by_hackathon(self, hackathon_id: int) -> list[ReminderSubscription]:
        stmt = select(ReminderSubscriptionORM).where(
            ReminderSubscriptionORM.hackathon_id == hackathon_id
        )
        items = (await self.session.execute(stmt)).scalars().all()
        return [to_dataclass(ReminderSubscription, o.__dict__) for o in items]

    async def get_subscribed_users(self, hackathon_id: int) -> list[User]:
        stmt = (
            select(UserORM)
            .join(ReminderSubscriptionORM, ReminderSubscriptionORM.user_id == UserORM.id)
            .where(
                ReminderSubscriptionORM.hackathon_id == hackathon_id,
                ReminderSubscriptionORM.enabled == True,  # noqa: E712
            )
        )
        users = (await self.session.execute(stmt)).scalars().all()
        return [to_dataclass(User, u.__dict__) for u in users]

    async def count_subscribed_users(self, hackathon_id: int) -> int:
        stmt = select(func.count(ReminderSubscriptionORM.id)).where(
            ReminderSubscriptionORM.hackathon_id == hackathon_id,
            ReminderSubscriptionORM.enabled == True,  # noqa: E712
        )
        return int((await self.session.execute(stmt)).scalar_one())

    async def count_all_subscribed(self) -> int:
        stmt = select(func.count(ReminderSubscriptionORM.id)).where(
            ReminderSubscriptionORM.enabled == True  # noqa: E712
        )
        return int((await self.session.execute(stmt)).scalar_one())
