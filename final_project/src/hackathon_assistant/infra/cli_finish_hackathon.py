from __future__ import annotations

import asyncio
import logging

from .db import get_session
from .usecase_provider import build_use_case_provider

logger = logging.getLogger(__name__)


async def run(hackathon_id: int) -> None:
    async with get_session() as session:
        uc = build_use_case_provider(session)
        await uc.finish_hackathon.execute(hackathon_id)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    import sys

    if len(sys.argv) < 2:
        raise SystemExit(
            "Usage: python -m hackathon_assistant.infra.cli_finish_hackathon <hackathon_id>"
        )

    asyncio.run(run(int(sys.argv[1])))


if __name__ == "__main__":
    main()
