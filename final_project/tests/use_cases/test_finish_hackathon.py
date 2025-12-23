from datetime import datetime, timedelta

import pytest

from hackathon_assistant.domain.models import Hackathon, ReminderSubscription


class TestFinishHackathonUseCase:
    """Тесты для FinishHackathonUseCase"""

    @pytest.mark.asyncio
    async def test_finish_hackathon_success(
        self, use_case_finish_hackathon, mock_hackathon_repo, mock_subscription_repo
    ):
        """Успешное завершение хакатона"""
        hackathon_id = 5

        hackathon = Hackathon(
            id=5,
            code="HACK2024",
            name="Test Hackathon",
            is_active=True,
            start_at=datetime.now() - timedelta(days=1),
            end_at=datetime.now() + timedelta(hours=1),
        )
        mock_hackathon_repo.get_by_id.return_value = hackathon

        subscriptions = [
            ReminderSubscription(id=1, user_id=1, hackathon_id=5, enabled=True),
            ReminderSubscription(id=2, user_id=2, hackathon_id=5, enabled=True),
            ReminderSubscription(id=3, user_id=3, hackathon_id=5, enabled=False),
        ]
        mock_subscription_repo.get_by_hackathon.return_value = subscriptions

        result = await use_case_finish_hackathon.execute(hackathon_id=hackathon_id)

        mock_hackathon_repo.get_by_id.assert_called_once_with(hackathon_id)
        mock_subscription_repo.get_by_hackathon.assert_called_once_with(hackathon_id)

        saved_hackathon = mock_hackathon_repo.save.call_args[0][0]
        assert saved_hackathon.is_active is False

        assert mock_subscription_repo.save.call_count == 3

        call_args_list = mock_subscription_repo.save.call_args_list
        for _i, call_args in enumerate(call_args_list):
            subscription = call_args[0][0]
            assert subscription.enabled is False

        assert result is True

    @pytest.mark.asyncio
    async def test_finish_hackathon_not_found(
        self, use_case_finish_hackathon, mock_hackathon_repo, mock_subscription_repo
    ):
        """Хакатон не найден"""
        hackathon_id = 999

        mock_hackathon_repo.get_by_id.return_value = None

        result = await use_case_finish_hackathon.execute(hackathon_id=hackathon_id)

        assert result is False
        mock_subscription_repo.get_by_hackathon.assert_not_called()
        mock_hackathon_repo.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_finish_hackathon_already_inactive(
        self, use_case_finish_hackathon, mock_hackathon_repo, mock_subscription_repo
    ):
        """Хакатон уже неактивен"""
        hackathon_id = 5

        hackathon = Hackathon(
            id=5,
            code="HACK2024",
            name="Test Hackathon",
            is_active=False,
            start_at=datetime.now() - timedelta(days=2),
            end_at=datetime.now() - timedelta(days=1),
        )
        mock_hackathon_repo.get_by_id.return_value = hackathon

        subscriptions = [
            ReminderSubscription(id=1, user_id=1, hackathon_id=5, enabled=False),  # уже отключена
        ]
        mock_subscription_repo.get_by_hackathon.return_value = subscriptions

        result = await use_case_finish_hackathon.execute(hackathon_id=hackathon_id)

        assert result is True

        mock_hackathon_repo.save.assert_called_once()

        mock_subscription_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_finish_hackathon_no_subscriptions(
        self, use_case_finish_hackathon, mock_hackathon_repo, mock_subscription_repo
    ):
        """Нет подписок на хакатон"""
        hackathon_id = 5

        hackathon = Hackathon(id=5, code="HACK2024", name="Test Hackathon", is_active=True)
        mock_hackathon_repo.get_by_id.return_value = hackathon

        mock_subscription_repo.get_by_hackathon.return_value = []

        result = await use_case_finish_hackathon.execute(hackathon_id=hackathon_id)

        assert result is True
        mock_hackathon_repo.save.assert_called_once()
        mock_subscription_repo.save.assert_not_called()
