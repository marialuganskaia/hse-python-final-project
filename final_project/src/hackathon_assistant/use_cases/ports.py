from dataclasses import dataclass
from typing import Protocol

from ..domain.models import Event, FAQItem, Hackathon, ReminderSubscription, Rules, User

# ========== Репозитории ==========


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

    async def get_all(self) -> list[User]:
        """Получить всех пользователей"""
        ...

    async def get_by_hackathon(self, hackathon_id: int) -> list[User]:
        """Получить пользователей по хакатону"""
        ...


class HackathonRepository(Protocol):
    """Для сценариев: /start (выбор), /hackathon (список), /schedule, /rules, /faq"""

    async def get_by_code(self, code: str) -> Hackathon | None:
        """Найти хакатон по коду (выбор по коду в /start)"""
        ...

    async def get_all_active(self) -> list[Hackathon]:
        """Получить все активные хакатоны (список для выбора в /hackathon)"""
        ...

    async def get_by_id(self, hackathon_id: int) -> Hackathon | None:
        """Получить хакатон по ID"""
        ...

    async def save(self, hackathon: Hackathon) -> Hackathon:
        """Сохранить хакатон (создать или обновить)"""
        ...


class EventRepository(Protocol):
    """Для сценариев: /schedule, напоминания"""

    async def get_by_hackathon(self, hackathon_id: int) -> list[Event]:
        """Получить все события хакатона (/schedule)"""
        ...

    async def get_upcoming_events(self, hackathon_id: int, hours_ahead: int) -> list[Event]:
        """Получить предстоящие события (для напоминаний)"""
        ...

    async def save_all(self, events: list[Event]) -> list[Event]:
        ...


class FAQRepository(Protocol):
    """Для сценариев: /faq"""

    async def get_by_hackathon(self, hackathon_id: int) -> list[FAQItem]:
        """Получить все FAQ хакатона (/faq)"""
        ...

    async def save_all(self, faq_items: list[FAQItem]) -> list[FAQItem]:
        ...


class RulesRepository(Protocol):
    """Для сценариев: /rules"""

    async def get_for_hackathon(self, hackathon_id: int) -> Rules | None:
        """Получить правила хакатона (/rules)"""
        ...

    async def save(self, rules: Rules) -> Rules:
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

    async def get_by_hackathon(self, hackathon_id: int) -> list[ReminderSubscription]:
        """Получить все подписки по хакатону"""
        ...


class Notifier(Protocol):
    async def send(self, telegram_id: int, text: str) -> None:
        ...


# ========== Request/Response модели для use cases ==========


@dataclass
class StartRequest:
    """Запрос для команды /start"""

    telegram_id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None


@dataclass
class StartResponse:
    """Ответ для команды /start"""

    welcome_message: str
    user_id: int
    hackathon_id: int | None = None


@dataclass
class ScheduleRequest:
    """Запрос для команды /schedule"""

    user_id: int


@dataclass
class ScheduleResponse:
    """Ответ для команды /schedule"""

    events: list[Event]


@dataclass
class RulesRequest:
    """Запрос для команды /rules"""

    user_id: int


@dataclass
class RulesResponse:
    """Ответ для команды /rules"""

    rules: Rules


@dataclass
class FAQRequest:
    """Запрос для команды /faq"""

    user_id: int


@dataclass
class FAQResponse:
    """Ответ для команды /faq"""

    faq_items: list[FAQItem]


@dataclass
class NotificationToggleRequest:
    """Запрос для команд /notify_on, /notify_off"""

    user_id: int
    enable: bool


@dataclass
class NotificationToggleResponse:
    """Ответ для команд /notify_on, /notify_off"""

    success: bool
    current_status: bool


# @dataclass
# class AdminStatsRequest:
#     """Запрос для команды /admin_stats"""
#
#     admin_user_id: int
#
#
# @dataclass
# class AdminStatsResponse:
#     """Ответ для команды /admin_stats"""
#
#     total_users: int
#     users_in_current_hackathon: int
#     subscribed_users: int


@dataclass
class BroadcastRequest:
    """Запрос для команды /admin_broadcast"""

    admin_user_id: int
    message: str


@dataclass
class BroadcastResponse:
    """Ответ для команды /admin_broadcast"""

    sent_count: int
    failed_count: int
