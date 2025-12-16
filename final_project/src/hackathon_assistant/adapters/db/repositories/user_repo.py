from __future__ import annotations

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ....domain.models import User
from ....use_cases.ports import UserRepository
from ..models import UserORM
from ..repositories_base import SQLAlchemyRepository
from .mappers import to_dataclass


class UserRepo(SQLAlchemyRepository, UserRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        stmt = select(UserORM).where(UserORM.telegram_id == telegram_id)
        orm_obj = (await self.session.execute(stmt)).scalars().first()
        if orm_obj is None:
            return None
        return to_dataclass(User, orm_obj.__dict__)

    async def save(self, user: User) -> User:
        # upsert по id (если есть) иначе insert
        if getattr(user, "id", None) is None:
            orm_obj = UserORM(
                telegram_id=user.telegram_id,
                username=getattr(user, "username", "") or "",
                first_name=getattr(user, "first_name", "") or "",
                last_name=getattr(user, "last_name", "") or "",
                role=user.role,
                current_hackathon_id=getattr(user, "current_hackathon_id", None),
            )
            self.session.add(orm_obj)
            await self.session.commit()
            await self.session.refresh(orm_obj)
            return to_dataclass(User, orm_obj.__dict__)

        # update existing
        stmt = (
            update(UserORM)
            .where(UserORM.id == user.id)
            .values(
                username=getattr(user, "username", "") or "",
                first_name=getattr(user, "first_name", "") or "",
                last_name=getattr(user, "last_name", "") or "",
                role=user.role,
                current_hackathon_id=getattr(user, "current_hackathon_id", None),
            )
        )
        await self.session.execute(stmt)
        await self.session.commit()
        return user

    async def update_current_hackathon(self, user_id: int, hackathon_id: int) -> None:
        stmt = (
            update(UserORM).where(UserORM.id == user_id).values(current_hackathon_id=hackathon_id)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    # --- методы для админки
    async def count_all(self) -> int:
        stmt = select(func.count(UserORM.id))
        return int((await self.session.execute(stmt)).scalar_one())

    async def count_by_hackathon(self, hackathon_id: int) -> int:
        stmt = select(func.count(UserORM.id)).where(UserORM.current_hackathon_id == hackathon_id)
        return int((await self.session.execute(stmt)).scalar_one())

    async def get_all(self) -> list[User]:
        stmt = select(UserORM)
        items = (await self.session.execute(stmt)).scalars().all()
        return [to_dataclass(User, o.__dict__) for o in items]

    async def get_by_hackathon(self, hackathon_id: int) -> list[User]:
        stmt = select(UserORM).where(UserORM.current_hackathon_id == hackathon_id)
        items = (await self.session.execute(stmt)).scalars().all()
        return [to_dataclass(User, o.__dict__) for o in items]
