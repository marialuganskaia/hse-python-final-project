from unittest.mock import AsyncMock

import pytest

from final_project.src.hackathon_assistant.domain.models import UserRole
from final_project.src.hackathon_assistant.use_cases.start_user import StartUserUseCase


class TestStartUserUseCase:
    """Тесты для StartUserUseCase."""

    @pytest.mark.asyncio
    async def test_execute_new_user(self, mock_user_repo):
        """Тест регистрации нового пользователя."""
        mock_user_repo.get_by_telegram_id.return_value = None
        mock_user_repo.save = AsyncMock()
        saved_user = mock_user_repo.save.return_value

        use_case = StartUserUseCase(user_repo=mock_user_repo)
        telegram_id = 123456789
        username = "testuser"
        first_name = "Test"
        last_name = "User"

        result = await use_case.execute(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        mock_user_repo.get_by_telegram_id.assert_called_once_with(telegram_id)
        mock_user_repo.save.assert_called_once()
        saved_user_arg = mock_user_repo.save.call_args[0][0]
        assert saved_user_arg.telegram_id == telegram_id
        assert saved_user_arg.username == username
        assert saved_user_arg.first_name == first_name
        assert saved_user_arg.last_name == last_name
        assert saved_user_arg.role == UserRole.PARTICIPANT
        assert result == saved_user

    @pytest.mark.asyncio
    async def test_execute_existing_user(self, mock_user_repo, sample_user):
        """Тест обновления существующего пользователя."""
        mock_user_repo.get_by_telegram_id.return_value = sample_user
        mock_user_repo.save = AsyncMock()
        saved_user = mock_user_repo.save.return_value

        use_case = StartUserUseCase(user_repo=mock_user_repo)
        telegram_id = 123456789
        new_username = "updateduser"
        new_first_name = "Updated"
        new_last_name = "User"

        result = await use_case.execute(
            telegram_id=telegram_id,
            username=new_username,
            first_name=new_first_name,
            last_name=new_last_name,
        )

        mock_user_repo.get_by_telegram_id.assert_called_once_with(telegram_id)
        mock_user_repo.save.assert_called_once()
        saved_user_arg = mock_user_repo.save.call_args[0][0]
        assert saved_user_arg.username == new_username
        assert saved_user_arg.first_name == new_first_name
        assert saved_user_arg.last_name == new_last_name
        assert result == saved_user
