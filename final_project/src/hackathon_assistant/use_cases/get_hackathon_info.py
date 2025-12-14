from dataclasses import dataclass
from typing import Optional, Tuple
from .ports import UserRepository, HackathonRepository, SubscriptionRepository
from .dto import HackathonDTO

@dataclass
class GetHackathonInfoUseCase:
    """Use case для команды /hackathon"""
    
    user_repo: UserRepository
    hackathon_repo: HackathonRepository
    subscription_repo: SubscriptionRepository

    async def execute(self, telegram_id: int) -> Tuple[Optional[HackathonDTO], bool]:
        """
        Получить информацию о текущем хакатоне пользователя и статус подписки
        Возвращает: (информация о хакатоне, статус подписки)
        """
        # TODO: реализовать
        pass