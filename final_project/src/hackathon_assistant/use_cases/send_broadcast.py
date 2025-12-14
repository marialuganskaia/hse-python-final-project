from dataclasses import dataclass
from typing import List
from .ports import UserRepository, SubscriptionRepository
from .dto import BroadcastTargetDTO


@dataclass
class SendBroadcastUseCase:
    user_repo: UserRepository
    subscription_repo: SubscriptionRepository

    async def execute(self, hackathon_id: int) -> List[BroadcastTargetDTO]:
        """Получить список пользователей для рассылки по хакатону"""
        subscriptions = await self.subscription_repo.get_by_hackathon(hackathon_id)
        active_subscriptions = [s for s in subscriptions if s.enabled]
        user_ids = {sub.user_id for sub in active_subscriptions}
        users = await self.user_repo.get_by_hackathon(hackathon_id)
        subscribed_users = [u for u in users if u.id in user_ids]
        return [
            BroadcastTargetDTO(
                telegram_id=user.telegram_id,
                user_id=user.id,
                first_name=user.first_name,
                username=user.username,
            )
            for user in subscribed_users]
