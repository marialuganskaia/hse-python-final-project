from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyRepository:
    """
    Base class for SQLAlchemy repositories (adapters layer).
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    def session(self) -> AsyncSession:
        return self._session
