import pytest
import asyncio
from unittest.mock import patch, Mock, AsyncMock
from final_project.src.hackathon_assistant.infra.db import db_ping, get_engine, dispose_engine


@pytest.mark.asyncio
async def test_db_ping_success():
    """Тест успешной проверки подключения к БД"""

    # Мокаем сессию
    mock_session = AsyncMock()

    # Создаем Mock для результата
    mock_result = Mock()
    mock_result.scalar_one.return_value = 1

    # Настраиваем execute
    mock_session.execute.return_value = mock_result

    with patch('final_project.src.hackathon_assistant.infra.db.get_session') as mock_get_session:
        mock_get_session.return_value.__aenter__.return_value = mock_session

        result = await db_ping()
        assert result is True


@pytest.mark.asyncio
async def test_db_ping_failure():
    """Тест неудачной проверки подключения к БД"""

    with patch('final_project.src.hackathon_assistant.infra.db.get_session') as mock_get_session:
        mock_get_session.return_value.__aenter__.side_effect = Exception("DB error")

        result = await db_ping()
        assert result is False


def test_get_engine():
    """Тест получения engine"""

    # Мокаем настройки
    with patch('final_project.src.hackathon_assistant.infra.db.get_settings') as mock_settings:
        mock_settings.return_value.database_url = "sqlite+aiosqlite:///:memory:"

        # Первый вызов создает engine
        engine1 = get_engine()
        assert engine1 is not None

        # Второй вызов возвращает тот же engine
        engine2 = get_engine()
        assert engine1 is engine2

        # Очищаем engine
        asyncio.run(dispose_engine())
