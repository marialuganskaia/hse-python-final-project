# from dataclasses import dataclass
# from typing import Optional
# from .ports import UserRepository, SubscriptionRepository
# from ..domain.models import ReminderSubscription
#
#
# @dataclass
# class SubscribeNotificationsUseCase:
#     user_repo: UserRepository
#     subscription_repo: SubscriptionRepository
#
#     async def execute(self, telegram_id: int) -> bool:
#         """ Включить напоминания для текущего хакатона пользователя
#             На вход telegram_id: ID пользователя в tg
#             Возвращаем bool: True если успешно, False если ошибка
#         """
#         user = await self.user_repo.get_by_telegram_id(telegram_id)
#         if user is None or user.current_hackathon_id is None:
#             return False
#
#         await self.subscription_repo.subscribe(
#             user_id=user.id,
#             hackathon_id=user.current_hackathon_id
#         )
#         return True
#
#
# @dataclass
# class UnsubscribeNotificationsUseCase:
#     user_repo: UserRepository
#     subscription_repo: SubscriptionRepository
#
#     async def execute(self, telegram_id: int) -> bool:
#         user = await self.user_repo.get_by_telegram_id(telegram_id)
#         if user is None or user.current_hackathon_id is None:
#             return False
#
#         # Просто вызываем unsubscribe
#         await self.subscription_repo.unsubscribe(
#             user_id=user.id,
#             hackathon_id=user.current_hackathon_id
#         )
#         return True