from dataclasses import dataclass

from ..domain.models import UserRole
from .dto import AdminStatsDTO
from .ports import HackathonRepository, SubscriptionRepository, UserRepository


@dataclass
class GetAdminStatsUseCase:
    user_repo: UserRepository
    subscription_repo: SubscriptionRepository
    hackathon_repo: HackathonRepository

    async def execute(self, hackathon_id: int) -> AdminStatsDTO | None:
        """Получить статистику для администратора
        Возвращает AdminStatsDTO: статистика по пользователям, подпискам
        """
        hackathon = await self.hackathon_repo.get_by_id(hackathon_id)
        if hackathon is None:
            return None
        total_users = await self.user_repo.count_by_hackathon(hackathon_id)
        users = await self.user_repo.get_by_hackathon(hackathon_id)
        participants = sum(1 for u in users if u.role == UserRole.PARTICIPANT)
        organizers = sum(1 for u in users if u.role == UserRole.ORGANIZER)
        subscribed_users = await self.subscription_repo.count_subscribed_users(hackathon_id)

        return AdminStatsDTO(
            total_users=total_users,
            participants=participants,
            organizers=organizers,
            subscribed_users=subscribed_users,
        )
