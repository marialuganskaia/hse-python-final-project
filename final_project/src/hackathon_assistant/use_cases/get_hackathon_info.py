from dataclasses import dataclass

from .dto import HackathonDTO
from .ports import HackathonRepository, SubscriptionRepository, UserRepository


@dataclass
class GetHackathonInfoUseCase:
    """Use case для команды /hackathon"""

    user_repo: UserRepository
    hackathon_repo: HackathonRepository
    subscription_repo: SubscriptionRepository

    async def execute(self, telegram_id: int) -> tuple[HackathonDTO | None, bool]:
        """
        Получить информацию о текущем хакатоне пользователя и статус подписки
        Возвращает: (информация о хакатоне, статус подписки)
        """
        # TODO: реализовать
        pass
