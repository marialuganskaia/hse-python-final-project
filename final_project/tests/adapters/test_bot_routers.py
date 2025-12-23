from unittest.mock import patch, MagicMock

import pytest
from aiogram import Dispatcher

from hackathon_assistant.adapters.bot.routers import setup_routers
from hackathon_assistant.adapters.bot.user import user_router, cmd_start,\
    cmd_help, cmd_schedule, cmd_join_hackathon
from hackathon_assistant.adapters.bot.admin import admin_router, cmd_admin_stats


class TestBotRouters:
    """Тесты роутеров бота"""

    def test_setup_routers(self):
        """Тест настройки роутеров"""
        dp = MagicMock(spec=Dispatcher)

        setup_routers(dp)

        dp.include_router.assert_any_call(user_router)
        dp.include_router.assert_any_call(admin_router)
        assert dp.include_router.call_count == 2

    @pytest.mark.asyncio
    async def test_cmd_start_handler(self, mock_message, mock_use_cases):
        """Тест обработчика команды /start"""

        mock_message.text = "/start"
        mock_use_cases.start_user.execute.return_value = MagicMock()

        await cmd_start(mock_message, mock_use_cases)

        mock_message.answer.assert_called_once()
        mock_use_cases.start_user.execute.assert_called_once_with(
            telegram_id=mock_message.from_user.id,
            username=mock_message.from_user.username,
            first_name=mock_message.from_user.first_name,
            last_name=mock_message.from_user.last_name,
        )

    @pytest.mark.asyncio
    async def test_cmd_help_handler(self, mock_message, mock_use_cases):
        """Тест обработчика команды /help"""

        mock_message.text = "/help"

        await cmd_help(mock_message, mock_use_cases)

        mock_message.answer.assert_called_once()
        assert "ℹ️ *Доступные команды:*" in mock_message.answer.call_args[0][0]

    @pytest.mark.asyncio
    async def test_cmd_schedule_with_hackathon_selected(self, mock_message, mock_use_cases):
        """Тест команды /schedule при выбранном хакатоне"""

        mock_message.text = "/schedule"

        with patch('final_project.src.hackathon_assistant.adapters.bot.user.require_hackathon_selected') as mock_check:
            mock_check.return_value = True
            mock_use_cases.get_schedule.execute.return_value = []

            await cmd_schedule(mock_message, mock_use_cases)

            mock_message.answer.assert_called_once()
            assert "📅 *Расписание:*" in mock_message.answer.call_args[0][0]

    @pytest.mark.asyncio
    async def test_cmd_join_valid_code(self, mock_message, mock_use_cases):
        """Тест команды /join с валидным кодом"""

        mock_message.text = "/join HACK2025"
        mock_hackathon = MagicMock()
        mock_hackathon.name = "Тестовый хакатон"
        mock_use_cases.select_hackathon_by_code.execute.return_value = mock_hackathon

        await cmd_join_hackathon(mock_message, mock_use_cases)

        mock_use_cases.select_hackathon_by_code.execute.assert_called_once_with(
            telegram_id=mock_message.from_user.id,
            hackathon_code="HACK2025"
        )
        mock_message.answer.assert_called_once()
        assert "✅ *Успешно!*" in mock_message.answer.call_args[0][0]
        assert "Тестовый хакатон" in mock_message.answer.call_args[0][0]

    @pytest.mark.asyncio
    async def test_cmd_join_missing_code(self, mock_message, mock_use_cases):
        """Тест команды /join без кода"""

        mock_message.text = "/join"

        await cmd_join_hackathon(mock_message, mock_use_cases)

        mock_message.answer.assert_called_once()
        assert "❌ *Использование:*" in mock_message.answer.call_args[0][0]
        assert "/join <код_хакатона>" in mock_message.answer.call_args[0][0]

    @pytest.mark.asyncio
    async def test_admin_stats_as_organizer(self, mock_message, mock_use_cases):
        """Тест команды /admin_stats для организатора"""

        mock_message.text = "/admin_stats"

        with patch('final_project.src.hackathon_assistant.adapters.bot.admin.is_organizer') as mock_is_organizer:
            mock_is_organizer.return_value = True
            mock_stats = MagicMock()
            mock_stats.total_users = 100
            mock_use_cases.get_admin_stats.execute.return_value = mock_stats

            await cmd_admin_stats(mock_message, mock_use_cases)

            mock_message.answer.assert_called_once()
            assert "100" in mock_message.answer.call_args[0][0]

    @pytest.mark.asyncio
    async def test_admin_stats_as_participant(self, mock_message, mock_use_cases):
        """Тест команды /admin_stats для участника"""

        mock_message.text = "/admin_stats"

        with patch('final_project.src.hackathon_assistant.adapters.bot.admin.is_organizer') as mock_is_organizer:
            mock_is_organizer.return_value = False

            await cmd_admin_stats(mock_message, mock_use_cases)

            mock_message.answer.assert_called_once()
            assert "❌ Эта команда доступна только организаторам" in mock_message.answer.call_args[0][0]
