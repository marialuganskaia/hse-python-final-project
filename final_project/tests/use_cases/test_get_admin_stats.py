import pytest

from final_project.src.hackathon_assistant.domain.models import User, UserRole
from final_project.src.hackathon_assistant.use_cases.dto import AdminStatsDTO


class TestGetAdminStatsUseCase:
    """Тесты для GetAdminStatsUseCase"""

    @pytest.mark.asyncio
    async def test_get_admin_stats(
        self, use_case_admin_stats, mock_user_repo, mock_subscription_repo, mock_hackathon_repo
    ):
        """Получение статистики"""
        mock_user_repo.count_all.return_value = 100

        users = [
            User(id=1, telegram_id=111, username="user1", role=UserRole.PARTICIPANT),
            User(id=2, telegram_id=222, username="user2", role=UserRole.PARTICIPANT),
            User(id=3, telegram_id=333, username="org1", role=UserRole.ORGANIZER),
            User(id=4, telegram_id=444, username="org2", role=UserRole.ORGANIZER),
            User(id=5, telegram_id=555, username="user3", role=UserRole.PARTICIPANT),
        ]
        mock_user_repo.get_all.return_value = users

        mock_subscription_repo.count_all_subscribed.return_value = 75

        result = await use_case_admin_stats.execute()

        mock_user_repo.count_all.assert_called_once()
        mock_user_repo.get_all.assert_called_once()
        mock_subscription_repo.count_all_subscribed.assert_called_once()

        assert isinstance(result, AdminStatsDTO)
        assert result.total_users == 100
        assert result.participants == 3
        assert result.organizers == 2
        assert result.subscribed_users == 75

    @pytest.mark.asyncio
    async def test_get_admin_stats_empty(
        self, use_case_admin_stats, mock_user_repo, mock_subscription_repo, mock_hackathon_repo
    ):
        """Статистика при отсутствии данных"""
        mock_user_repo.count_all.return_value = 0
        mock_user_repo.get_all.return_value = []
        mock_subscription_repo.count_all_subscribed.return_value = 0

        result = await use_case_admin_stats.execute()

        assert result.total_users == 0
        assert result.participants == 0
        assert result.organizers == 0
        assert result.subscribed_users == 0

    @pytest.mark.asyncio
    async def test_count_all_subscribed_method(self, use_case_admin_stats, mock_subscription_repo):
        """Проверка вызова count_all_subscribed"""
        mock_subscription_repo.count_all_subscribed.return_value = 42

        result = await use_case_admin_stats.execute()

        mock_subscription_repo.count_all_subscribed.assert_called_once()
        assert result.subscribed_users == 42

    @pytest.mark.asyncio
    async def test_get_admin_stats_only_participants(
        self, use_case_admin_stats, mock_user_repo, mock_subscription_repo, mock_hackathon_repo
    ):
        """Только участники, без организаторов"""
        mock_user_repo.count_all.return_value = 50

        users = [
            User(id=i, telegram_id=i * 100, username=f"user{i}", role=UserRole.PARTICIPANT)
            for i in range(1, 51)
        ]
        mock_user_repo.get_all.return_value = users

        mock_subscription_repo.count_all_subscribed.return_value = 30

        result = await use_case_admin_stats.execute()

        assert result.total_users == 50
        assert result.participants == 50
        assert result.organizers == 0
        assert result.subscribed_users == 30

    @pytest.mark.asyncio
    async def test_get_admin_stats_only_organizers(
        self, use_case_admin_stats, mock_user_repo, mock_subscription_repo, mock_hackathon_repo
    ):
        """Только организаторы"""
        mock_user_repo.count_all.return_value = 10

        users = [
            User(id=i, telegram_id=i * 100, username=f"org{i}", role=UserRole.ORGANIZER)
            for i in range(1, 11)
        ]
        mock_user_repo.get_all.return_value = users

        mock_subscription_repo.count_all_subscribed.return_value = 5

        result = await use_case_admin_stats.execute()

        assert result.total_users == 10
        assert result.participants == 0
        assert result.organizers == 10
        assert result.subscribed_users == 5
