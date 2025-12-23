from dataclasses import dataclass

from ..domain.models import UserRole
from .dto import AdminStatsDTO
from .ports import HackathonRepository, SubscriptionRepository, UserRepository


@dataclass
class GetAdminStatsUseCase:
    user_repo: UserRepository
    subscription_repo: SubscriptionRepository
    hackathon_repo: HackathonRepository

    async def execute(self) -> AdminStatsDTO:
        """Получить общую статистику (по всем хакатонам)"""
        total_users = await self.user_repo.count_all()
        users = await self.user_repo.get_all()
        participants = sum(1 for u in users if u.role == UserRole.PARTICIPANT)
        organizers = sum(1 for u in users if u.role == UserRole.ORGANIZER)
        subscribed_users = await self.subscription_repo.count_all_subscribed()

        return AdminStatsDTO(
            total_users=total_users,
            participants=participants,
            organizers=organizers,
            subscribed_users=subscribed_users,
        )
