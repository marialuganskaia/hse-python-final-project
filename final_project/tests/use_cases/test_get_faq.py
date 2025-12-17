import pytest

from final_project.src.hackathon_assistant.use_cases.dto import FAQItemDTO
from final_project.src.hackathon_assistant.use_cases.get_faq import GetFAQUseCase


class TestGetFAQUseCase:
    """Тесты для GetFAQUseCase."""

    @pytest.mark.asyncio
    async def test_execute_with_faq(self, mock_user_repo, mock_faq_repo, sample_user, sample_faq_item):
        """Тест получения FAQ."""
        mock_user_repo.get_by_telegram_id.return_value = sample_user
        mock_faq_repo.get_by_hackathon.return_value = [sample_faq_item]

        use_case = GetFAQUseCase(
            user_repo=mock_user_repo,
            faq_repo=mock_faq_repo
        )
        telegram_id = 123456789

        result = await use_case.execute(telegram_id)

        mock_user_repo.get_by_telegram_id.assert_called_once_with(telegram_id)
        mock_faq_repo.get_by_hackathon.assert_called_once_with(sample_user.current_hackathon_id)
        assert len(result) == 1
        assert isinstance(result[0], FAQItemDTO)
        assert result[0].question == sample_faq_item.question
        assert result[0].answer == sample_faq_item.answer

    @pytest.mark.asyncio
    async def test_execute_no_user(self, mock_user_repo, mock_faq_repo):
        """Тест получения FAQ для несуществующего пользователя."""
        mock_user_repo.get_by_telegram_id.return_value = None

        use_case = GetFAQUseCase(
            user_repo=mock_user_repo,
            faq_repo=mock_faq_repo
        )
        telegram_id = 999999999

        result = await use_case.execute(telegram_id)

        mock_user_repo.get_by_telegram_id.assert_called_once_with(telegram_id)
        mock_faq_repo.get_by_hackathon.assert_not_called()
        assert result == []

    @pytest.mark.asyncio
    async def test_execute_no_hackathon(self, mock_user_repo, mock_faq_repo, sample_user):
        """Тест получения FAQ для пользователя без хакатона."""
        sample_user.current_hackathon_id = None
        mock_user_repo.get_by_telegram_id.return_value = sample_user

        use_case = GetFAQUseCase(
            user_repo=mock_user_repo,
            faq_repo=mock_faq_repo
        )
        telegram_id = 123456789

        result = await use_case.execute(telegram_id)

        mock_user_repo.get_by_telegram_id.assert_called_once_with(telegram_id)
        mock_faq_repo.get_by_hackathon.assert_not_called()
        assert result == []

    @pytest.mark.asyncio
    async def test_execute_sorted_by_id(self, mock_user_repo, mock_faq_repo, sample_user):
        """Тест сортировки FAQ по ID."""
        faq1 = sample_user.copy()
        faq1.id = 3
        faq1.question = "Question 3"
        faq2 = sample_user.copy()
        faq2.id = 1
        faq2.question = "Question 1"
        faq3 = sample_user.copy()
        faq3.id = 2
        faq3.question = "Question 2"

        mock_user_repo.get_by_telegram_id.return_value = sample_user
        mock_faq_repo.get_by_hackathon.return_value = [faq1, faq2, faq3]

        use_case = GetFAQUseCase(
            user_repo=mock_user_repo,
            faq_repo=mock_faq_repo
        )

        result = await use_case.execute(sample_user.telegram_id)

        assert len(result) == 3
        assert result[0].id == 1
        assert result[1].id == 2
        assert result[2].id == 3