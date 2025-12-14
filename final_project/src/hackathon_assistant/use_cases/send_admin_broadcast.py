from dataclasses import dataclass
from typing import Optional
from .ports import UserRepository, SubscriptionRepository
from .dto import BroadcastResultDTO


@dataclass
class SendAdminBroadcastUseCase:
    """Use case для команды /admin_broadcast"""
    
    user_repo: UserRepository
    subscription_repo: SubscriptionRepository

    async def execute(self, admin_user_id: int, message: str, hackathon_id: Optional[int] = None) -> BroadcastResultDTO:
        """
        Отправить рассылку сообщения администратором
        Возвращает: результат рассылки
        """
        # TODO: реализовать
        pass
