import pytest

from hackathon_assistant.domain.models import FAQItem
from hackathon_assistant.use_cases.dto import FAQItemDTO
from hackathon_assistant.use_cases.get_faq import GetFAQUseCase


class TestGetFAQUseCase:
    """Тесты для GetFAQUseCase."""

    @pytest.mark.asyncio
    async def test_execute_with_faq(
        self, mock_user_repo, mock_faq_repo, sample_user, sample_faq_item
    ):
        """Тест получения FAQ."""
        mock_user_repo.get_by_telegram_id.return_value = sample_user
        mock_faq_repo.get_by_hackathon.return_value = [sample_faq_item]

        use_case = GetFAQUseCase(user_repo=mock_user_repo, faq_repo=mock_faq_repo)
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

        use_case = GetFAQUseCase(user_repo=mock_user_repo, faq_repo=mock_faq_repo)
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

        use_case = GetFAQUseCase(user_repo=mock_user_repo, faq_repo=mock_faq_repo)
        telegram_id = 123456789

        result = await use_case.execute(telegram_id)

        mock_user_repo.get_by_telegram_id.assert_called_once_with(telegram_id)
        mock_faq_repo.get_by_hackathon.assert_not_called()
        assert result == []

    @pytest.mark.asyncio
    async def test_execute_sorted_by_id(self, mock_user_repo, mock_faq_repo, sample_user):
        """Тест сортировки FAQ по ID."""
        mock_user_repo.get_by_telegram_id.return_value = sample_user

        faq1 = FAQItem(
            id=2,
            hackathon_id=sample_user.current_hackathon_id,
            question="Q2",
            answer="A2",
        )
        faq2 = FAQItem(
            id=1,
            hackathon_id=sample_user.current_hackathon_id,
            question="Q1",
            answer="A1",
        )
        mock_faq_repo.get_by_hackathon.return_value = [faq1, faq2]

        use_case = GetFAQUseCase(user_repo=mock_user_repo, faq_repo=mock_faq_repo)
        result = await use_case.execute(sample_user.telegram_id)

        assert [x.question for x in result] == ["Q1", "Q2"]
