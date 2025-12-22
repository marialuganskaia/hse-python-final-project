import pytest

from final_project.src.hackathon_assistant.domain.models import ReminderSubscription, User, UserRole
from final_project.src.hackathon_assistant.use_cases.dto import BroadcastTargetDTO


class TestSendBroadcastUseCase:
    """Тесты для SendBroadcastUseCase"""

    @pytest.mark.asyncio
    async def test_get_broadcast_targets(
        self, use_case_send_broadcast, mock_user_repo, mock_subscription_repo
    ):
        """Получение списка получателей для рассылки"""
        hackathon_id = 5

        subscriptions = [
            ReminderSubscription(id=1, user_id=1, hackathon_id=5, enabled=True),
            ReminderSubscription(id=2, user_id=2, hackathon_id=5, enabled=True),
            ReminderSubscription(id=3, user_id=3, hackathon_id=5, enabled=False),
            ReminderSubscription(id=4, user_id=4, hackathon_id=5, enabled=True),
        ]
        mock_subscription_repo.get_by_hackathon.return_value = subscriptions

        users = [
            User(
                id=1,
                telegram_id=111,
                username="user1",
                first_name="Alice",
                role=UserRole.PARTICIPANT,
            ),
            User(
                id=2, telegram_id=222, username="user2", first_name="Bob", role=UserRole.PARTICIPANT
            ),
            User(
                id=3,
                telegram_id=333,
                username="user3",
                first_name="Charlie",
                role=UserRole.PARTICIPANT,
            ),
            User(
                id=4,
                telegram_id=444,
                username="user4",
                first_name="Diana",
                role=UserRole.PARTICIPANT,
            ),
            User(
                id=5, telegram_id=555, username="user5", first_name="Eve", role=UserRole.PARTICIPANT
            ),
        ]
        mock_user_repo.get_by_hackathon.return_value = users

        result = await use_case_send_broadcast.execute(
            hackathon_id=hackathon_id, message="Test broadcast"
        )

        mock_subscription_repo.get_by_hackathon.assert_called_once_with(hackathon_id)
        mock_user_repo.get_by_hackathon.assert_called_once_with(hackathon_id)

        assert isinstance(result, list)
        assert len(result) == 3

        user_ids = {target.user_id for target in result}
        assert 1 in user_ids
        assert 2 in user_ids
        assert 4 in user_ids
        assert 3 not in user_ids
        assert 5 not in user_ids

        target = result[0]
        assert isinstance(target, BroadcastTargetDTO)
        assert target.user_id == 1
        assert target.telegram_id == 111
        assert target.username == "user1"
        assert target.first_name == "Alice"

    @pytest.mark.asyncio
    async def test_get_broadcast_targets_no_subscriptions(
        self, use_case_send_broadcast, mock_user_repo, mock_subscription_repo
    ):
        """Нет активных подписок"""
        hackathon_id = 5

        mock_subscription_repo.get_by_hackathon.return_value = []  # нет подписок
        mock_user_repo.get_by_hackathon.return_value = [
            User(id=1, telegram_id=111, username="user1")
        ]

        result = await use_case_send_broadcast.execute(hackathon_id=hackathon_id, message="Test")

        assert result == []

    @pytest.mark.asyncio
    async def test_get_broadcast_targets_only_disabled_subscriptions(
        self, use_case_send_broadcast, mock_user_repo, mock_subscription_repo
    ):
        """Только отключенные подписки"""
        hackathon_id = 5

        subscriptions = [
            ReminderSubscription(id=1, user_id=1, hackathon_id=5, enabled=False),
            ReminderSubscription(id=2, user_id=2, hackathon_id=5, enabled=False),
        ]
        mock_subscription_repo.get_by_hackathon.return_value = subscriptions

        users = [
            User(id=1, telegram_id=111, username="user1"),
            User(id=2, telegram_id=222, username="user2"),
        ]
        mock_user_repo.get_by_hackathon.return_value = users

        result = await use_case_send_broadcast.execute(hackathon_id=hackathon_id, message="Test")

        assert result == []

    @pytest.mark.asyncio
    async def test_get_broadcast_targets_user_not_found_for_subscription(
        self, use_case_send_broadcast, mock_user_repo, mock_subscription_repo
    ):
        """Пользователь не найден для активной подписки"""
        hackathon_id = 5

        subscriptions = [
            ReminderSubscription(id=1, user_id=1, hackathon_id=5, enabled=True),
            ReminderSubscription(
                id=2, user_id=999, hackathon_id=5, enabled=True
            ),  # несуществующий user_id
        ]
        mock_subscription_repo.get_by_hackathon.return_value = subscriptions

        users = [
            User(id=1, telegram_id=111, username="user1"),
        ]
        mock_user_repo.get_by_hackathon.return_value = users

        result = await use_case_send_broadcast.execute(hackathon_id=hackathon_id, message="Test")

        assert len(result) == 1
        assert result[0].user_id == 1

    @pytest.mark.asyncio
    async def test_get_broadcast_targets_empty_users(
        self, use_case_send_broadcast, mock_user_repo, mock_subscription_repo
    ):
        """Нет пользователей в хакатоне"""
        hackathon_id = 5

        subscriptions = [
            ReminderSubscription(id=1, user_id=1, hackathon_id=5, enabled=True),
        ]
        mock_subscription_repo.get_by_hackathon.return_value = subscriptions

        mock_user_repo.get_by_hackathon.return_value = []  # нет пользователей

        result = await use_case_send_broadcast.execute(hackathon_id=hackathon_id, message="Test")

        assert result == []
