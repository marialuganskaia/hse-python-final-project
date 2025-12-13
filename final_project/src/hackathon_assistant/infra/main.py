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
    """
    Entrypoint (skeleton).
    Сейчас: settings + db_ping + wiring middleware + роутеры.
    Позже: scheduler + полноценные handlers + репозитории Dev2.
    """
    settings = get_settings()
    logger.info("Starting app. DATABASE_URL=%s", settings.database_url)

    if not await db_ping():
        logger.error("DB ping failed. Check DATABASE_URL and DB availability.")
        return
    logger.info("DB ping OK.")

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    # use cases per update: session -> UseCaseProvider -> handler data["use_cases"]
    dp.update.outer_middleware(
        UseCasesMiddleware(
            session_cm_factory=get_session,
            provider_factory=build_use_case_provider,
            data_key="use_cases",
        )
    )

    setup_routers(dp)

    # Пока Dev3 не сделал хендлеры, polling можно запускать, но командами бот не ответит.
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
