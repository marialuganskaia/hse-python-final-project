from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from ..use_cases.ports import (
    HackathonRepository, 
    UserRepository,
    EventRepository,
    FAQRepository,
    RulesRepository,
    SubscriptionRepository
)


@dataclass(frozen=True)
class RepositoryProvider:
    """
    Repository provider (infra wiring).
    """

    session: AsyncSession

    def user_repo(self) -> UserRepository:
        return UserRepo(self.session)

    def hackathon_repo(self) -> HackathonRepository:
        raise NotImplementedError("Dev2: implement SQLAlchemy HackathonRepository and wire here")

    # ДОБАВЬ ЭТИ МЕТОДЫ:
    def event_repo(self) -> EventRepository:
        raise NotImplementedError("Dev2: implement SQLAlchemy EventRepository and wire here")

    def rules_repo(self) -> RulesRepository:
        raise NotImplementedError("Dev2: implement SQLAlchemy RulesRepository and wire here")

    def faq_repo(self) -> FAQRepository:
        raise NotImplementedError("Dev2: implement SQLAlchemy FAQRepository and wire here")

    def subscription_repo(self) -> SubscriptionRepository:
        raise NotImplementedError("Dev2: implement SQLAlchemy SubscriptionRepository and wire here")
