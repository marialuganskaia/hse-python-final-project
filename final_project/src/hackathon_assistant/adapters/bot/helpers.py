from typing import Optional
from hackathon_assistant.infra.usecase_provider import UseCaseProvider


async def is_organizer(telegram_id: int, use_cases: UseCaseProvider) -> bool:
    """
    Проверяет, является ли пользователь организатором
    
    Args:
        telegram_id: ID пользователя в Telegram
        use_cases: провайдер use cases
        
    Returns:
        True если пользователь организатор, False в противном случае
    """
    try:
        user = await use_cases.get_user_by_telegram_id(telegram_id)
        return user is not None and user.role == "organizer"
    except Exception:
        return False


async def get_current_hackathon_id(telegram_id: int, use_cases: UseCaseProvider) -> Optional[int]:
    """
    Получает ID текущего хакатона пользователя
    
    Args:
        telegram_id: ID пользователя в Telegram
        use_cases: провайдер use cases
        
    Returns:
        ID хакатона или None
    """
    try:
        user = await use_cases.get_user_by_telegram_id(telegram_id)
        return user.current_hackathon_id if user else None
    except Exception:
        return None
