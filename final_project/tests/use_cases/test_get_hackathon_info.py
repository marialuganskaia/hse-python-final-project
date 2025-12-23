from datetime import datetime, timedelta

import pytest

from final_project.src.hackathon_assistant.domain.models import Hackathon, ReminderSubscription, User, UserRole
from final_project.src.hackathon_assistant.use_cases.dto import HackathonDTO


class TestGetHackathonInfoUseCase:
    """Тесты для GetHackathonInfoUseCase"""

    @pytest.mark.asyncio
    async def test_get_hackathon_info_success_with_active_subscription(
        self,
        use_case_get_hackathon_info,
        mock_user_repo,
        mock_hackathon_repo,
        mock_subscription_repo,
        sample_hackathon,
    ):
        """Успешное получение информации о хакатоне с активной подпиской"""
        user = User(id=1, telegram_id=123456789, username="test_user", current_hackathon_id=1)
        mock_user_repo.get_by_telegram_id.return_value = user

        mock_hackathon_repo.get_by_id.return_value = sample_hackathon

        subscription = ReminderSubscription(id=1, user_id=1, hackathon_id=1, enabled=True)
        mock_subscription_repo.get_user_subscription.return_value = subscription

        result = await use_case_get_hackathon_info.execute(telegram_id=123456789)

        mock_user_repo.get_by_telegram_id.assert_called_once_with(123456789)
        mock_hackathon_repo.get_by_id.assert_called_once_with(1)
        mock_subscription_repo.get_user_subscription.assert_called_once_with(
            user_id=1, hackathon_id=1
        )

        hackathon_dto, is_subscribed = result
        assert isinstance(hackathon_dto, HackathonDTO)
        assert hackathon_dto.name == "Test Hackathon"
        assert hackathon_dto.code == "HACK2024"
        assert hackathon_dto.description == "Test description"
        assert hackathon_dto.location == "Test Location"
        assert hackathon_dto.is_active is True
        assert is_subscribed is True

    @pytest.mark.asyncio
    async def test_get_hackathon_info_success_without_subscription(
        self,
        use_case_get_hackathon_info,
        mock_user_repo,
        mock_hackathon_repo,
        mock_subscription_repo,
        sample_hackathon,
    ):
        """Успешное получение информации о хакатоне без подписки"""
        user = User(id=1, telegram_id=123456789, username="test_user", current_hackathon_id=1)
        mock_user_repo.get_by_telegram_id.return_value = user

        mock_hackathon_repo.get_by_id.return_value = sample_hackathon

        mock_subscription_repo.get_user_subscription.return_value = None

        result = await use_case_get_hackathon_info.execute(telegram_id=123456789)

        hackathon_dto, is_subscribed = result
        assert isinstance(hackathon_dto, HackathonDTO)
        assert hackathon_dto.name == "Test Hackathon"
        assert is_subscribed is False

    @pytest.mark.asyncio
    async def test_get_hackathon_info_success_with_inactive_subscription(
        self,
        use_case_get_hackathon_info,
        mock_user_repo,
        mock_hackathon_repo,
        mock_subscription_repo,
        sample_hackathon,
    ):
        """Успешное получение информации о хакатоне с неактивной подпиской"""
        user = User(id=1, telegram_id=123456789, username="test_user", current_hackathon_id=1)
        mock_user_repo.get_by_telegram_id.return_value = user

        mock_hackathon_repo.get_by_id.return_value = sample_hackathon

        subscription = ReminderSubscription(id=1, user_id=1, hackathon_id=1, enabled=False)
        mock_subscription_repo.get_user_subscription.return_value = subscription

        result = await use_case_get_hackathon_info.execute(telegram_id=123456789)

        hackathon_dto, is_subscribed = result
        assert isinstance(hackathon_dto, HackathonDTO)
        assert is_subscribed is False

    @pytest.mark.asyncio
    async def test_get_hackathon_info_user_not_found(
        self,
        use_case_get_hackathon_info,
        mock_user_repo,
        mock_hackathon_repo,
        mock_subscription_repo,
    ):
        """Пользователь не найден"""
        mock_user_repo.get_by_telegram_id.return_value = None

        result = await use_case_get_hackathon_info.execute(telegram_id=999999)

        hackathon_dto, is_subscribed = result
        assert hackathon_dto is None
        assert is_subscribed is False

        mock_hackathon_repo.get_by_id.assert_not_called()
        mock_subscription_repo.get_user_subscription.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_hackathon_info_no_hackathon_selected(
        self,
        use_case_get_hackathon_info,
        mock_user_repo,
        mock_hackathon_repo,
        mock_subscription_repo,
    ):
        """У пользователя нет выбранного хакатона"""
        user = User(id=1, telegram_id=123456789, username="test_user", current_hackathon_id=None)
        mock_user_repo.get_by_telegram_id.return_value = user

        result = await use_case_get_hackathon_info.execute(telegram_id=123456789)

        hackathon_dto, is_subscribed = result
        assert hackathon_dto is None
        assert is_subscribed is False

        mock_hackathon_repo.get_by_id.assert_not_called()
        mock_subscription_repo.get_user_subscription.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_hackathon_info_hackathon_not_found(
        self,
        use_case_get_hackathon_info,
        mock_user_repo,
        mock_hackathon_repo,
        mock_subscription_repo,
    ):
        """Хакатон не найден"""
        user = User(id=1, telegram_id=123456789, username="test_user", current_hackathon_id=999)
        mock_user_repo.get_by_telegram_id.return_value = user

        mock_hackathon_repo.get_by_id.return_value = None

        result = await use_case_get_hackathon_info.execute(telegram_id=123456789)

        hackathon_dto, is_subscribed = result
        assert hackathon_dto is None
        assert is_subscribed is False

        mock_hackathon_repo.get_by_id.assert_called_once_with(999)
        mock_subscription_repo.get_user_subscription.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_hackathon_info_all_fields_mapped(
        self,
        use_case_get_hackathon_info,
        mock_user_repo,
        mock_hackathon_repo,
        mock_subscription_repo,
        sample_hackathon,
    ):
        """Проверка что все поля хакатона правильно мапятся в DTO"""
        user = User(id=1, telegram_id=123456789, username="test_user", current_hackathon_id=1)
        mock_user_repo.get_by_telegram_id.return_value = user

        mock_hackathon_repo.get_by_id.return_value = sample_hackathon

        mock_subscription_repo.get_user_subscription.return_value = None

        result = await use_case_get_hackathon_info.execute(telegram_id=123456789)

        hackathon_dto, is_subscribed = result

        assert hackathon_dto.id == sample_hackathon.id
        assert hackathon_dto.name == sample_hackathon.name
        assert hackathon_dto.code == sample_hackathon.code
        assert hackathon_dto.description == sample_hackathon.description
        assert hackathon_dto.start_at == sample_hackathon.start_at
        assert hackathon_dto.end_at == sample_hackathon.end_at
        assert hackathon_dto.location == sample_hackathon.location
        assert hackathon_dto.is_active == sample_hackathon.is_active
        assert is_subscribed is False

    @pytest.mark.asyncio
    async def test_get_hackathon_info_inactive_hackathon(
        self,
        use_case_get_hackathon_info,
        mock_user_repo,
        mock_hackathon_repo,
        mock_subscription_repo,
    ):
        """Получение информации о неактивном хакатоне"""
        now = datetime.now()
        inactive_hackathon = Hackathon(
            id=3,
            code="OLD2023",
            name="Old Hackathon",
            description="Completed hackathon",
            start_at=now - timedelta(days=30),
            end_at=now - timedelta(days=27),
            is_active=False,
            location="Old Location",
        )

        user = User(id=1, telegram_id=123456789, username="test_user", current_hackathon_id=3)
        mock_user_repo.get_by_telegram_id.return_value = user
        mock_hackathon_repo.get_by_id.return_value = inactive_hackathon
        mock_subscription_repo.get_user_subscription.return_value = None

        result = await use_case_get_hackathon_info.execute(telegram_id=123456789)

        hackathon_dto, is_subscribed = result

        assert hackathon_dto.name == "Old Hackathon"
        assert hackathon_dto.is_active is False
        assert is_subscribed is False

    @pytest.mark.asyncio
    async def test_get_hackathon_info_organizer_user(
        self,
        use_case_get_hackathon_info,
        mock_user_repo,
        mock_hackathon_repo,
        mock_subscription_repo,
        sample_hackathon,
    ):
        """Организатор получает информацию о хакатоне"""
        organizer = User(
            id=99,
            telegram_id=999999999,
            username="organizer",
            first_name="Admin",
            last_name="User",
            role=UserRole.ORGANIZER,
            current_hackathon_id=1,
        )

        mock_user_repo.get_by_telegram_id.return_value = organizer
        mock_hackathon_repo.get_by_id.return_value = sample_hackathon

        mock_subscription_repo.get_user_subscription.return_value = None

        result = await use_case_get_hackathon_info.execute(telegram_id=999999999)

        hackathon_dto, is_subscribed = result

        assert hackathon_dto.name == "Test Hackathon"
        assert is_subscribed is False
