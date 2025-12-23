from dataclasses import dataclass

from .dto import BroadcastTargetDTO
from .ports import SubscriptionRepository, UserRepository


@dataclass
class SendAdminBroadcastUseCase:
    """Use case для команды /admin_broadcast"""

    user_repo: UserRepository
    subscription_repo: SubscriptionRepository

    async def execute(
        self, admin_user_id: int, message: str, hackathon_id: int | None = None
    ) -> list[BroadcastTargetDTO]:
        """
        Отправить рассылку сообщения администратором
        """
        users = await self.subscription_repo.get_subscribed_users(hackathon_id)

        return [
            BroadcastTargetDTO(
                user_id=user.id,
                telegram_id=user.telegram_id,
                username=user.username or "",
                first_name=user.first_name or "",
            )
            for user in users
        ]
