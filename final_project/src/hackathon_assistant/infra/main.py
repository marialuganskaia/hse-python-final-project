from __future__ import annotations

import asyncio
import logging

from .db import db_ping
from .settings import get_settings

logger = logging.getLogger(__name__)


async def main() -> None:
    """
    Application entrypoint.

    План инициализации:
      1) settings (env/.env)
      2) init DB: async engine + sessionmaker (lazy in infra/db.py)
      3) init repositories (adapters/db)       (Dev2)
      4) init use-cases provider (infra wiring) (Dev1 later)
      5) init bot: Bot + Dispatcher + routers  (Dev3)
      6) init scheduler for reminders          (Dev1 later)
      7) start polling
    """
    settings = get_settings()
    logger.info("Starting app. DATABASE_URL=%s", settings.database_url)

    ok = await db_ping()
    if not ok:
        logger.error("DB ping failed. Check DATABASE_URL and DB availability.")
        return

    logger.info("DB ping OK.")

    # TODO(Dev2): repositories implementations (SQLAlchemy adapters)
    # TODO(Dev1): use-cases provider wiring (DI)
    # TODO(Dev3): routers registration
    # TODO(Dev1): scheduler integration


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
