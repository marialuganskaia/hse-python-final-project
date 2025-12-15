from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from ..adapters.db.repositories import (
    EventRepo,
    FAQRepo,
    HackathonRepo,
    RulesRepo,
    SubscriptionRepo,
    UserRepo,
)
from ..use_cases.ports import (
    EventRepository,
    FAQRepository,
    HackathonRepository,
    RulesRepository,
    SubscriptionRepository,
    UserRepository,
)


@dataclass(frozen=True)
class RepositoryProvider:
    session: AsyncSession

    def user_repo(self) -> UserRepository:
        return UserRepo(self.session)

    def hackathon_repo(self) -> HackathonRepository:
        return HackathonRepo(self.session)

    def event_repo(self) -> EventRepository:
        return EventRepo(self.session)

    def rules_repo(self) -> RulesRepository:
        return RulesRepo(self.session)

    def faq_repo(self) -> FAQRepository:
        return FAQRepo(self.session)

    def subscription_repo(self) -> SubscriptionRepository:
        return SubscriptionRepo(self.session)
