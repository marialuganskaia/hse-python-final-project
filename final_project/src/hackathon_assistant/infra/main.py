from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher

from ..adapters.bot.middlewares.usecases import UseCasesMiddleware
from ..adapters.bot.routers import setup_routers
from .db import db_ping, get_session
from .settings import get_settings
from .usecase_provider import build_use_case_provider

logger = logging.getLogger(__name__)


async def main() -> None:
    settings = get_settings()
    logger.info("Starting app. DATABASE_URL=%s", settings.database_url)

    if not await db_ping():
        logger.error("DB ping failed. Check DATABASE_URL and DB availability.")
        return
    logger.info("DB ping OK.")

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    from sqlalchemy.ext.asyncio import AsyncSession

    def provider_factory(session: AsyncSession):
        return build_use_case_provider(session=session, bot=bot)

    dp.update.outer_middleware(
        UseCasesMiddleware(
            session_cm_factory=get_session,
            provider_factory=provider_factory,
            data_key="use_cases",
        )
    )

    setup_routers(dp)

    reminder_service = None
    try:
        from ..adapters.bot.reminders import ReminderService

        REMINDERS_ENABLED = True
    except ImportError:
        REMINDERS_ENABLED = False
        logger.warning("ReminderService not found, reminders disabled")

    if REMINDERS_ENABLED:
        try:
            from ..adapters.bot.reminders import ReminderService

            reminder_service = ReminderService(bot, build_use_case_provider)

            if settings.reminders_enabled:
                await reminder_service.start_periodic_reminders(
                    interval_minutes=settings.reminder_interval_minutes
                )
            logger.info("Reminder service started")

        except Exception as e:
            logger.error(f"Failed to start reminder service: {e}")
            reminder_service = None

    logger.info("Starting bot polling...")
    try:
        await dp.start_polling(bot)
    finally:
        if reminder_service:
            await reminder_service.stop_periodic_reminders()
            logger.info("Reminder service stopped")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
