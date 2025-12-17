from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hackathon_assistant.infra.usecase_provider import UseCaseProvider


async def is_organizer(telegram_id: int, use_cases: UseCaseProvider) -> bool:
    """
    Проверяет, является ли пользователь организатором

    TODO: Заменить на реальную проверку
    """
    # ВРЕМЕННАЯ ЗАГЛУШКА для тестирования
    # Разрешаем всем для тестирования UX
    return True

    # Или проверка по конкретным ID:
    # allowed_ids = [123456789]  # ваш Telegram ID
    # return telegram_id in allowed_ids


async def get_current_hackathon_id(telegram_id: int, use_cases: UseCaseProvider) -> int | None:
    """
    Получает ID текущего хакатона пользователя
    """
    # ВРЕМЕННАЯ ЗАГЛУШКА
    return 1  # ID тестового хакатона
