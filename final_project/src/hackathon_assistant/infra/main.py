from __future__ import annotations

import asyncio
import logging

from .settings import get_settings

logger = logging.getLogger(__name__)


async def main() -> None:
    settings = get_settings()
    logger.info("Starting app. DATABASE_URL=%s", settings.database_url)
    # TODO : init db engine/session, init bot/dispatcher, routers, scheduler


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
