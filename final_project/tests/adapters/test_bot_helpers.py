from unittest.mock import patch, MagicMock

import pytest

from hackathon_assistant.adapters.bot.helpers import (
    is_organizer,
)
from hackathon_assistant.domain.models import UserRole


class TestBotHelpers:
    """Тесты вспомогательных функций"""

    @pytest.mark.asyncio
    async def test_is_organizer_by_allowed_ids(self, mock_use_cases):
        """Тест проверки организатора по allowed_admin_ids"""

        telegram_id = 123456789

        with patch('final_project.src.hackathon_assistant.adapters.bot.helpers.get_settings') as mock_settings:
            settings = MagicMock()
            settings.allowed_admin_ids = [telegram_id, 987654321]
            mock_settings.return_value = settings

            result = await is_organizer(telegram_id, mock_use_cases)

            assert result is True

    @pytest.mark.asyncio
    async def test_is_organizer_by_role(self, mock_use_cases):
        """Тест проверки организатора по роли в БД"""
        telegram_id = 123456789
        mock_user = MagicMock()
        mock_user.role = UserRole.ORGANIZER
        mock_use_cases.start_user.user_repo.get_by_telegram_id.return_value = mock_user

        with patch('final_project.src.hackathon_assistant.adapters.bot.helpers.get_settings') as mock_settings:
            settings = MagicMock()
            settings.allowed_admin_ids = []
            mock_settings.return_value = settings

            result = await is_organizer(telegram_id, mock_use_cases)

            assert result is True
            mock_use_cases.start_user.user_repo.get_by_telegram_id.assert_called_once_with(telegram_id)

    @pytest.mark.asyncio
    async def test_is_not_organizer(self, mock_use_cases):
        """Тест, что участник не является организатором"""
        telegram_id = 123456789
        mock_user = MagicMock()
        mock_user.role = UserRole.PARTICIPANT
        mock_use_cases.start_user.user_repo.get_by_telegram_id.return_value = mock_user

        with patch('final_project.src.hackathon_assistant.adapters.bot.helpers.get_settings') as mock_settings:
            settings = MagicMock()
            settings.allowed_admin_ids = []
            mock_settings.return_value = settings

            result = await is_organizer(telegram_id, mock_use_cases)

            assert result is False

    @pytest.mark.asyncio
    async def test_is_organizer_user_not_found(self, mock_use_cases):
        """Тест, когда пользователь не найден в БД"""
        telegram_id = 999999999
        mock_use_cases.start_user.user_repo.get_by_telegram_id.return_value = None

        with patch('final_project.src.hackathon_assistant.adapters.bot.helpers.get_settings') as mock_settings:
            settings = MagicMock()
            settings.allowed_admin_ids = []
            mock_settings.return_value = settings

            result = await is_organizer(telegram_id, mock_use_cases)

            assert result is False
