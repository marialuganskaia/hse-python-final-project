"""
Черновые интерфейсы репозиториев
На основе сценариев из документации
"""

from typing import Protocol

from ..domain.models import Event, FAQItem, Hackathon, ReminderSubscription, Rules, User


class UserRepository(Protocol):
    """Для сценариев: /start (регистрация), /hackathon (смена), /admin_stats"""

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        """Найти пользователя по telegram_id (для /start)"""
        ...

    async def save(self, user: User) -> User:
        """Сохранить нового пользователя (регистрация в /start)"""
        ...

    async def update_current_hackathon(self, user_id: int, hackathon_id: int) -> None:
        """Обновить текущий хакатон пользователя (/hackathon)"""
        ...

    async def count_all(self) -> int:
        """Подсчитать всех пользователей (/admin_stats)"""
        ...

    async def count_by_hackathon(self, hackathon_id: int) -> int:
        """Подсчитать пользователей по хакатону (/admin_stats)"""
        ...


class HackathonRepository(Protocol):
    """Для сценариев: /start (выбор), /hackathon (список), /schedule, /rules, /faq"""

    async def get_by_code(self, code: str) -> Hackathon | None:
        """Найти хакатон по коду (выбор по коду в /start)"""
        ...

    async def get_all_active(self) -> list[Hackathon]:
        """Получить все активные хакатоны (список для выбора в /hackathon)"""
        ...

    # async def get_by_id(self, hackathon_id: int) -> Optional[Hackathon]
    #     """Получить хакатон по ID (для получения текущего хакатона пользователя)."""
    #     ... вопрос в избыточности????


class EventRepository(Protocol):
    """Для сценариев: /schedule, напоминания"""

    async def get_by_hackathon(self, hackathon_id: int) -> list[Event]:
        """Получить все события хакатона (/schedule)"""
        ...

    async def get_upcoming_events(self, hackathon_id: int, hours_ahead: int) -> list[Event]:
        """Получить предстоящие события (для напоминаний)"""
        ...


class FAQRepository(Protocol):
    """Для сценариев: /faq"""

    async def get_by_hackathon(self, hackathon_id: int) -> list[FAQItem]:
        """Получить все FAQ хакатона (/faq)"""
        ...


class RulesRepository(Protocol):
    """Для сценариев: /rules"""

    async def get_for_hackathon(self, hackathon_id: int) -> Rules | None:
        """Получить правила хакатона (/rules)"""
        ...


class SubscriptionRepository(Protocol):
    """Для сценариев: /notify_on, /notify_off, напоминания, /admin_stats"""

    async def get_user_subscription(
        self, user_id: int, hackathon_id: int
    ) -> ReminderSubscription | None:
        """Получить подписку пользователя на хакатон (/notify_on/off)"""
        ...

    # async def subscribe(self, user_id: int, hackathon_id: int) -> ReminderSubscription:
    #     """Создать/активировать подписку (/notify_on)."""
    #     ...
    #
    # async def unsubscribe(self, user_id: int, hackathon_id: int) -> None:
    #     """Отключить подписку (/notify_off)"""
    #     ... вроде избыточно, но это не точно

    async def get_subscribed_users(self, hackathon_id: int) -> list[User]:
        """Получить подписанных пользователей (для напоминаний)"""
        ...

    async def count_subscribed_users(self, hackathon_id: int) -> int:
        """Подсчитать подписанных пользователей (/admin_stats)"""
        ...

    async def save(self, subscription: ReminderSubscription) -> ReminderSubscription:
        """Сохранить подписку (сохранить или обновить)"""
        ...
