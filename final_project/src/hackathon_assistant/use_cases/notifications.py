from dataclasses import dataclass
from typing import Optional
from .ports import UserRepository, SubscriptionRepository
from ..domain.models import ReminderSubscription


@dataclass
class SubscribeNotificationsUseCase:
    user_repo: UserRepository
    subscription_repo: SubscriptionRepository

    async def execute(self, telegram_id: int) -> bool:
        """ Включить напоминания для текущего хакатона пользователя
            На вход telegram_id: ID пользователя в tg
            Возвращаем bool: True если успешно, False если ошибка
        """
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if user is None or user.current_hackathon_id is None:
            return False

        sub = await self.subscription_repo.subscribe(
            user_id=user.id,
            hackathon_id=user.current_hackathon_id
        )
        if sub is None:
            sub = ReminderSubscription(
                id=None,
                user_id=user.id,
                hackathon_id=user.current_hackathon_id,
                enabled=True
            )
        else:
            sub.enabled = True
        await self.subscription_repo.save(subscription=sub)
        return True


@dataclass
class UnsubscribeNotificationsUseCase:
    user_repo: UserRepository
    subscription_repo: SubscriptionRepository

    async def execute(self, telegram_id: int) -> bool:
        """ Выключить напоминания для текущего хакатона пользователя
            На вход telegram_id: ID пользователя в tg
            Возвращаем bool: True если успешно, False если ошибка
        """
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if user is None or user.current_hackathon_id is None:
            return False

        sub = await self.subscription_repo.get_user_subscription(
            user_id=user.id,
            hackathon_id=user.current_hackathon_id
        )
        if sub is None:
            return False
        sub.enabled = False
        await self.subscription_repo.save(subscription=sub)
        return True
