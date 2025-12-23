import asyncio
import logging

from aiogram import Bot

logger = logging.getLogger(__name__)


class ReminderService:
    """Сервис отправки напоминаний о событиях хакатона"""

    def __init__(self, bot: Bot, use_case_provider_factory):
        """
        Args:
            bot: экземпляр aiogram Bot
            use_case_provider_factory: фабрика для создания UseCaseProvider
        """
        self.bot = bot
        self.use_case_provider_factory = use_case_provider_factory
        self._task: asyncio.Task | None = None
        logger.info("ReminderService initialized")

    async def start_periodic_reminders(self, interval_minutes: int = 5):
        """Запускает периодическую проверку напоминаний"""
        if self._task and not self._task.done():
            logger.warning("Reminder task already running")
            return

        self._task = asyncio.create_task(self._periodic_reminder_task(interval_minutes))
        logger.info(f"Periodic reminders started (interval: {interval_minutes} min)")

    async def stop_periodic_reminders(self):
        """Останавливает периодические напоминания"""
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            logger.info("Periodic reminders stopped")

    async def _periodic_reminder_task(self, interval_minutes: int):
        """Фоновая задача для периодической проверки"""
        try:
            while True:
                await self.send_upcoming_event_reminders()
                await asyncio.sleep(interval_minutes * 60)
        except asyncio.CancelledError:
            logger.info("Reminder task cancelled")
        except Exception as e:
            logger.error(f"Reminder task error: {e}")

    async def send_upcoming_event_reminders(self):
        """Отправляет напоминания о предстоящих событиях"""
        logger.info("Checking for upcoming events...")

        try:
            # Проверяем доступность use cases
            # Это тестовая реализация для проверки структуры
            await self._send_test_reminder()

            # TODO: Реальная реализация, когда репозитории будут готовы:
            # async with self.use_case_provider_factory() as use_cases:
            #     # 1. Получить активные хакатоны
            #     hackathons = await use_cases.list_hackathons.execute(active_only=True)
            #
            #     for hackathon in hackathons:
            #         # 2. Получить события через 15 минут
            #         events = await use_cases.get_upcoming_events.execute(
            #             hackathon_id=hackathon.id,
            #             minutes_ahead=15
            #         )
            #
            #         for event in events:
            #             # 3. Получить подписанных пользователей
            #             # 4. Отправить напоминания

        except Exception as e:
            logger.error(f"Error in send_upcoming_event_reminders: {e}")

    async def _send_test_reminder(self):
        """Отправляет тестовое напоминание для проверки структуры"""
        try:
            # Импортируем DTO для теста
            from datetime import datetime, timedelta

            from hackathon_assistant.use_cases.dto import EventDTO

            # Создаем тестовое событие
            test_event = EventDTO(
                id=1,
                title="🎯 Тестовое событие",
                description="Это тестовое напоминание для проверки работы сервиса",
                starts_at=datetime.now() + timedelta(minutes=20),
                ends_at=datetime.now() + timedelta(hours=1),
                location="Главный зал",
            )

            # Тестовый пользователь (заглушка)
            class TestUser:
                telegram_id = 123456789  # Замените на реальный ID для теста

            # Отправляем тестовое напоминание
            await self.send_reminder_to_user(TestUser(), test_event, 20)
            logger.info("Test reminder structure verified")

        except ImportError as e:
            logger.warning(f"Cannot import DTO for test: {e}")
        except Exception as e:
            logger.error(f"Test reminder error: {e}")

    async def send_reminder_to_user(self, user, event, minutes_before: int):
        """Отправляет напоминание конкретному пользователю"""
        try:
            from .formatters import format_reminder_message

            message = format_reminder_message(event, minutes_before)

            await self.bot.send_message(user.telegram_id, message, parse_mode="Markdown")
            logger.info(f"Reminder sent to user {user.telegram_id}")

        except ImportError as e:
            logger.error(f"Format function not found: {e}")
        except Exception as e:
            logger.error(f"Failed to send reminder: {e}")
