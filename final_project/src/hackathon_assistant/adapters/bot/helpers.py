from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hackathon_assistant.infra.usecase_provider import UseCaseProvider

from hackathon_assistant.domain.models import UserRole
from hackathon_assistant.infra.settings import get_settings
from hackathon_assistant.infra.usecase_provider import UseCaseProvider


async def is_organizer(telegram_id: int, use_cases: UseCaseProvider) -> bool:
    """
    Проверяет, является ли пользователь организатором
    """
    settings = get_settings()

    # 1) Strict allow-list (if configured)
    if settings.allowed_admin_ids:
        return telegram_id in settings.allowed_admin_ids

    # 2) Fallback: role-based from DB
    user = await use_cases.start_user.user_repo.get_by_telegram_id(telegram_id)
    return user is not None and user.role == UserRole.ORGANIZER


async def get_current_hackathon_id(telegram_id: int, use_cases: UseCaseProvider) -> int | None:
    """
    Получает ID текущего хакатона пользователя
    """
    hackathon_dto, _ = await use_cases.get_hackathon_info.execute(telegram_id=telegram_id)
    return None if hackathon_dto is None else hackathon_dto.id
