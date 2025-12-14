from __future__ import annotations

from collections.abc import Awaitable, Callable
from contextlib import AbstractAsyncContextManager
from typing import Any

from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession


class UseCasesMiddleware(BaseMiddleware):
    """
    Builds UseCaseProvider per update and puts it into handler data.

    We pass factories from infra, so adapters/bot doesn't import infra.
    """

    def __init__(
        self,
        session_cm_factory: Callable[[], AbstractAsyncContextManager[AsyncSession]],
        provider_factory: Callable[[AsyncSession], Any],
        data_key: str = "use_cases",
    ) -> None:
        super().__init__()
        self._session_cm_factory = session_cm_factory
        self._provider_factory = provider_factory
        self._data_key = data_key

    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: dict[str, Any],
    ) -> Any:
        async with self._session_cm_factory() as session:
            data[self._data_key] = self._provider_factory(session)
            return await handler(event, data)
