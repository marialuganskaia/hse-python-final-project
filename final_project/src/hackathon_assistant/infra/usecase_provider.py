from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from ..use_cases.select_hackathon import SelectHackathonByCodeUseCase
from ..use_cases.start_user import StartUserUseCase
from .repositories import RepositoryProvider


@dataclass(frozen=True)
class UseCaseProvider:
    """Container with ready-to-use participant use cases."""

    start_user: StartUserUseCase
    select_hackathon_by_code: SelectHackathonByCodeUseCase


def build_use_case_provider(session: AsyncSession) -> UseCaseProvider:
    repos = RepositoryProvider(session=session)

    return UseCaseProvider(
        start_user=StartUserUseCase(user_repo=repos.user_repo()),
        select_hackathon_by_code=SelectHackathonByCodeUseCase(
            user_repo=repos.user_repo(),
            hackathon_repo=repos.hackathon_repo(),
        ),
    )
