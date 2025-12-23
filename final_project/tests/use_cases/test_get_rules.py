import pytest

from hackathon_assistant.use_cases.dto import RulesDTO
from hackathon_assistant.use_cases.get_rules import GetRulesUseCase


class TestGetRulesUseCase:
    """Тесты для GetRulesUseCase."""

    @pytest.mark.asyncio
    async def test_execute_with_rules(
        self, mock_user_repo, mock_rules_repo, sample_user, sample_rules
    ):
        """Тест получения правил."""
        mock_user_repo.get_by_telegram_id.return_value = sample_user
        mock_rules_repo.get_for_hackathon.return_value = sample_rules

        use_case = GetRulesUseCase(user_repo=mock_user_repo, rules_repo=mock_rules_repo)
        telegram_id = 123456789

        result = await use_case.execute(telegram_id)

        mock_user_repo.get_by_telegram_id.assert_called_once_with(telegram_id)
        mock_rules_repo.get_for_hackathon.assert_called_once_with(sample_user.current_hackathon_id)
        assert isinstance(result, RulesDTO)
        assert result.content == sample_rules.content

    @pytest.mark.asyncio
    async def test_execute_no_user(self, mock_user_repo, mock_rules_repo):
        """Тест получения правил для несуществующего пользователя."""
        mock_user_repo.get_by_telegram_id.return_value = None

        use_case = GetRulesUseCase(user_repo=mock_user_repo, rules_repo=mock_rules_repo)
        telegram_id = 999999999

        result = await use_case.execute(telegram_id)

        mock_user_repo.get_by_telegram_id.assert_called_once_with(telegram_id)
        mock_rules_repo.get_for_hackathon.assert_not_called()
        assert result is None

    @pytest.mark.asyncio
    async def test_execute_no_hackathon(self, mock_user_repo, mock_rules_repo, sample_user):
        """Тест получения правил для пользователя без хакатона."""
        sample_user.current_hackathon_id = None
        mock_user_repo.get_by_telegram_id.return_value = sample_user

        use_case = GetRulesUseCase(user_repo=mock_user_repo, rules_repo=mock_rules_repo)
        telegram_id = 123456789

        result = await use_case.execute(telegram_id)

        mock_user_repo.get_by_telegram_id.assert_called_once_with(telegram_id)
        mock_rules_repo.get_for_hackathon.assert_not_called()
        assert result is None

    @pytest.mark.asyncio
    async def test_execute_no_rules(self, mock_user_repo, mock_rules_repo, sample_user):
        """Тест получения правил, если правила не найдены."""
        mock_user_repo.get_by_telegram_id.return_value = sample_user
        mock_rules_repo.get_for_hackathon.return_value = None

        use_case = GetRulesUseCase(user_repo=mock_user_repo, rules_repo=mock_rules_repo)
        telegram_id = 123456789

        result = await use_case.execute(telegram_id)

        mock_user_repo.get_by_telegram_id.assert_called_once_with(telegram_id)
        mock_rules_repo.get_for_hackathon.assert_called_once_with(sample_user.current_hackathon_id)
        assert result is None
