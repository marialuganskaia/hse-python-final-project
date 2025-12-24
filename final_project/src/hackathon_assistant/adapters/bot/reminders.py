import asyncio
import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

logger = logging.getLogger(__name__)


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
        logger.info(f"Periodic reminders started (interval: {interval_minutes} min)")

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
            logger.error(f"Reminder task error: {e}")

    async def send_upcoming_event_reminders(self):
        logger.info("Checking for upcoming events (2h and 15min)...")
        try:
            async with self.use_case_provider_factory() as use_cases:
                hackathons = await use_cases.list_hackathons.execute(active_only=True)
                
                for hackathon in hackathons:
                    events_by_interval = await self._get_events_for_reminders(
                        use_cases, hackathon.id
                    )
                    
                    for interval_minutes, events in events_by_interval.items():
                        if events:
                            await self._send_reminders_for_interval(
                                use_cases, hackathon.id, events, interval_minutes
                            )
                            
        except Exception as e:
            logger.error(f"Error in send_upcoming_event_reminders: {e}")

    async def _get_events_for_reminders(self, use_cases, hackathon_id: int):
        from datetime import datetime, timedelta
        
        try:
            events = await use_cases.get_upcoming_events.execute(
                hackathon_id=hackathon_id,
                minutes_ahead=125
            )
            
            if not events:
                return {}
            
            now = datetime.now()
            result = {
                120: [],
                15: []
            }
            
            for event in events:
                minutes_until_start = (event.starts_at - now).total_seconds() / 60
                
                if 119 <= minutes_until_start <= 121:
                    result[120].append(event)
                elif 14 <= minutes_until_start <= 16:
                    result[15].append(event)
            
            return {k: v for k, v in result.items() if v}
            
        except Exception as e:
            logger.error(f"Error filtering events for reminders: {e}")
            return {}

    async def _send_reminders_for_interval(self, use_cases, hackathon_id: int, events: list, interval_minutes: int):
        if not events:
            return
            
        logger.info(f"Sending {interval_minutes}min reminders for {len(events)} events")
        
        try:
            subscribed_users = await use_cases.get_subscribed_users.execute(hackathon_id)
            
            for event in events:
                for user in subscribed_users:
                    try:
                        await self.send_reminder_to_user(user, event, interval_minutes)
                    except Exception as e:
                        logger.error(f"Failed to send reminder for event {event.id} to user {user.id}: {e}")
                        
        except Exception as e:
            logger.error(f"Error sending reminders for interval {interval_minutes}: {e}")

    async def send_reminder_to_user(self, user, event, minutes_before: int):
        try:
            from .formatters import format_reminder_message

            message = format_reminder_message(event, minutes_before)
            await self.bot.send_message(user.telegram_id, message, parse_mode="Markdown")
            logger.info(f"Reminder sent to user {user.telegram_id} for event: {event.title}")

        except TelegramBadRequest as e:
            if "chat not found" in str(e).lower() or "bot was blocked" in str(e).lower():
                logger.warning(f"User {user.telegram_id} not available: {e}")
            else:
                logger.error(f"Telegram error for user {user.telegram_id}: {e}")
        except TelegramForbiddenError as e:
            logger.warning(f"User {user.telegram_id} blocked the bot: {e}")
        except ImportError as e:
            logger.error(f"Format function not found: {e}")
        except Exception as e:
            logger.error(f"Failed to send reminder to user {user.telegram_id}: {e}")
        