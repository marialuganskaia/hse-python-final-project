from dataclasses import dataclass

from .dto import BroadcastResultDTO
from .ports import SubscriptionRepository, UserRepository


@dataclass
class SendAdminBroadcastUseCase:
    """Use case для команды /admin_broadcast"""

    user_repo: UserRepository
    subscription_repo: SubscriptionRepository

    async def execute(
        self, admin_user_id: int, message: str, hackathon_id: int | None = None
    ) -> BroadcastResultDTO:
        """
        Отправить рассылку сообщения администратором
        Возвращает: результат рассылки
        """
        # TODO: реализовать
        pass
