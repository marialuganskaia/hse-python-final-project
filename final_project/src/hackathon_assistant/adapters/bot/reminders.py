import asyncio
import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from hackathon_assistant.infra.db import get_session
from hackathon_assistant.use_cases.process_reminder import ProcessRemindersUseCase
from hackathon_assistant.use_cases.send_reminder import SendRemindersUseCase

logger = logging.getLogger(__name__)


class _AiogramNotifier:
    def __init__(self, bot: Bot):
        self._bot = bot

    async def send(self, telegram_id: int, text: str) -> None:
        try:
            await self._bot.send_message(telegram_id, text, parse_mode="Markdown")
        except TelegramBadRequest as e:
            msg = str(e).lower()
            if "chat not found" in msg or "bot was blocked" in msg:
                logger.warning("User %s not available: %s", telegram_id, e)
            else:
                logger.error("Telegram error for user %s: %s", telegram_id, e)
        except TelegramForbiddenError as e:
            logger.warning("User %s blocked the bot: %s", telegram_id, e)


class ReminderService:
    def __init__(self, bot: Bot, use_case_provider_factory):
        self.bot = bot
        self.use_case_provider_factory = use_case_provider_factory
        self._task: asyncio.Task | None = None
        logger.info("ReminderService initialized")

    async def start_periodic_reminders(self, interval_minutes: int = 5):
        if self._task and not self._task.done():
            logger.warning("Reminder task already running")
            return

        self._task = asyncio.create_task(self._periodic_reminder_task(interval_minutes))
        logger.info("Periodic reminders started (interval: %s min)", interval_minutes)

    async def stop_periodic_reminders(self):
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            logger.info("Periodic reminders stopped")

    async def _periodic_reminder_task(self, interval_minutes: int):
        try:
            while True:
                await self.send_upcoming_event_reminders()
                await asyncio.sleep(interval_minutes * 60)
        except asyncio.CancelledError:
            logger.info("Reminder task cancelled")
        except Exception as e:
            logger.error("Reminder task error: %s", e)

    async def send_upcoming_event_reminders(self):
        logger.info("Checking for upcoming events...")
        try:
            async with get_session() as session:
                use_cases = self.use_case_provider_factory(session)

                hackathons = await use_cases.list_hackathons.execute(active_only=True)
                if not hackathons:
                    logger.info("No active hackathons, skip reminders")
                    return

                process_uc = ProcessRemindersUseCase(
                    event_repo=use_cases.get_upcoming_events.event_repo,
                    subscription_repo=use_cases.subscribe_notifications.subscription_repo,
                )
                send_uc = SendRemindersUseCase(notifier=_AiogramNotifier(self.bot))

                all_piles = []
                for h in hackathons:
                    piles = await process_uc.execute(hackathon_id=h.id, hours_ahead=1)
                    all_piles.extend(piles)

                if not all_piles:
                    logger.info("No reminder piles, nothing to send")
                    return

                await send_uc.execute(all_piles)

        except Exception as e:
            logger.error(f"Error in send_upcoming_event_reminders: {e}")
