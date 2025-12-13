from __future__ import annotations

import asyncio
import logging

from .settings import get_settings

logger = logging.getLogger(__name__)


async def main() -> None:
    """
    Application entrypoint.

    План инициализации:
      1) settings (env/.env)
      2) init DB: async engine + sessionmaker
      3) init repositories (adapters/db)
      4) init use-cases provider (infra wiring)
      5) init bot: Bot + Dispatcher + routers (adapters/bot)
      6) init scheduler for reminders (infra)
      7) start polling
    """
    settings = get_settings()

    # Никогда не логируем BOT_TOKEN.
    logger.info("Starting app. DATABASE_URL=%s", settings.database_url)

    # TODO(Dev1): init async engine/sessionmaker
    # TODO(Dev2): repositories implementations (SQLAlchemy adapters)
    # TODO(Dev1): use-cases provider wiring (DI)
    # TODO(Dev3): routers registration
    # TODO(Dev1): scheduler integration

    return


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
