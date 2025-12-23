from unittest.mock import AsyncMock

import pytest

from hackathon_assistant.use_cases.select_hackathon import (
    SelectHackathonByCodeUseCase,
)


class TestSelectHackathonByCodeUseCase:
    """Тесты для SelectHackathonByCodeUseCase."""

    @pytest.mark.asyncio
    async def test_execute_success(
        self, mock_user_repo, mock_hackathon_repo, sample_user, sample_hackathon
    ):
        """Тест успешного выбора хакатона."""
        mock_user_repo.get_by_telegram_id.return_value = sample_user
        mock_hackathon_repo.get_by_code.return_value = sample_hackathon
        mock_user_repo.save = AsyncMock()

        use_case = SelectHackathonByCodeUseCase(
            user_repo=mock_user_repo, hackathon_repo=mock_hackathon_repo
        )
        telegram_id = 123456789
        hackathon_code = "HACK2024"

        result = await use_case.execute(telegram_id, hackathon_code)

        mock_user_repo.get_by_telegram_id.assert_called_once_with(telegram_id)
        mock_hackathon_repo.get_by_code.assert_called_once_with(hackathon_code)
        mock_user_repo.save.assert_called_once()
        saved_user = mock_user_repo.save.call_args[0][0]
        assert saved_user.current_hackathon_id == sample_hackathon.id
        assert result == sample_hackathon

    @pytest.mark.asyncio
    async def test_execute_user_not_found(
        self, mock_user_repo, mock_hackathon_repo, sample_hackathon
    ):
        """Тест выбора хакатона для несуществующего пользователя."""
        mock_user_repo.get_by_telegram_id.return_value = None

        use_case = SelectHackathonByCodeUseCase(
            user_repo=mock_user_repo, hackathon_repo=mock_hackathon_repo
        )
        result = await use_case.execute(telegram_id=999999999, hackathon_code="HACK2024")

        assert result is None
        mock_user_repo.get_by_telegram_id.assert_called_once_with(999999999)
        mock_hackathon_repo.get_by_code.assert_not_called()
