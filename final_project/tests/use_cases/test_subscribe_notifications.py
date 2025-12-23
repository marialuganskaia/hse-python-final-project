from unittest.mock import AsyncMock

import pytest

from hackathon_assistant.use_cases.notifications import (
    SubscribeNotificationsUseCase,
)


class TestSubscribeNotificationsUseCase:
    """Тесты для SubscribeNotificationsUseCase."""

    @pytest.mark.asyncio
    async def test_execute_new_subscription(
        self, mock_user_repo, mock_subscription_repo, sample_user
    ):
        """Тест создания новой подписки."""
        # Arrange
        mock_user_repo.get_by_telegram_id.return_value = sample_user
        mock_subscription_repo.get_user_subscription.return_value = None
        mock_subscription_repo.save = AsyncMock()

        use_case = SubscribeNotificationsUseCase(
            user_repo=mock_user_repo, subscription_repo=mock_subscription_repo
        )
        telegram_id = 123456789

        result = await use_case.execute(telegram_id)

        mock_user_repo.get_by_telegram_id.assert_called_once_with(telegram_id)
        mock_subscription_repo.get_user_subscription.assert_called_once_with(
            user_id=sample_user.id, hackathon_id=sample_user.current_hackathon_id
        )
        mock_subscription_repo.save.assert_called_once()
        args, kwargs = mock_subscription_repo.save.call_args
        saved_sub = args[0] if args else kwargs.get("subscription")
        assert saved_sub.user_id == sample_user.id
        assert saved_sub.hackathon_id == sample_user.current_hackathon_id
        assert saved_sub.enabled is True
        assert result is True

    @pytest.mark.asyncio
    async def test_execute_existing_subscription_enable(
        self, mock_user_repo, mock_subscription_repo, sample_user, sample_subscription
    ):
        """Тест включения существующей подписки."""
        sample_subscription.enabled = False
        mock_user_repo.get_by_telegram_id.return_value = sample_user
        mock_subscription_repo.get_user_subscription.return_value = sample_subscription
        mock_subscription_repo.save = AsyncMock()

        use_case = SubscribeNotificationsUseCase(
            user_repo=mock_user_repo, subscription_repo=mock_subscription_repo
        )
        telegram_id = 123456789

        result = await use_case.execute(telegram_id)

        mock_user_repo.get_by_telegram_id.assert_called_once_with(telegram_id)
        mock_subscription_repo.get_user_subscription.assert_called_once_with(
            user_id=sample_user.id, hackathon_id=sample_user.current_hackathon_id
        )
        mock_subscription_repo.save.assert_called_once()
        args, kwargs = mock_subscription_repo.save.call_args
        saved_sub = args[0] if args else kwargs.get("subscription")
        assert saved_sub.enabled is True
        assert result is True

    @pytest.mark.asyncio
    async def test_execute_no_user(self, mock_user_repo, mock_subscription_repo):
        """Тест попытки подписаться для несуществующего пользователя."""
        mock_user_repo.get_by_telegram_id.return_value = None

        use_case = SubscribeNotificationsUseCase(
            user_repo=mock_user_repo, subscription_repo=mock_subscription_repo
        )
        telegram_id = 999999999

        result = await use_case.execute(telegram_id)

        mock_user_repo.get_by_telegram_id.assert_called_once_with(telegram_id)
        mock_subscription_repo.get_user_subscription.assert_not_called()
        mock_subscription_repo.save.assert_not_called()
        assert result is False

    @pytest.mark.asyncio
    async def test_execute_no_hackathon(self, mock_user_repo, mock_subscription_repo, sample_user):
        """Тест попытки подписаться для пользователя без хакатона."""
        sample_user.current_hackathon_id = None
        mock_user_repo.get_by_telegram_id.return_value = sample_user

        use_case = SubscribeNotificationsUseCase(
            user_repo=mock_user_repo, subscription_repo=mock_subscription_repo
        )
        telegram_id = 123456789

        result = await use_case.execute(telegram_id)

        mock_user_repo.get_by_telegram_id.assert_called_once_with(telegram_id)
        mock_subscription_repo.get_user_subscription.assert_not_called()
        mock_subscription_repo.save.assert_not_called()
        assert result is False
