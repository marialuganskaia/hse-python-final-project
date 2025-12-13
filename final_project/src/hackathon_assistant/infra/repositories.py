from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass(frozen=True)
class RepositoryProvider:
    """
    Repository provider (infra wiring).

    Dev2 позже добавит конкретные репозитории (SQLAlchemy adapters)
    Dev1 будет собирать их в use-cases provider.
    """

    session: AsyncSession

    # Примеры -- заглушки:
    # def user_repo(self) -> UserRepository: ...
    # def hackathon_repo(self) -> HackathonRepository: ...
    # def event_repo(self) -> EventRepository: ...
    # def faq_repo(self) -> FAQRepository: ...
    # def rules_repo(self) -> RulesRepository: ...
    # def subscription_repo(self) -> SubscriptionRepository: ...
