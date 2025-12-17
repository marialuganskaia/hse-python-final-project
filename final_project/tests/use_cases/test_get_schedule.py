from datetime import datetime, timedelta, timezone

import pytest

from final_project.src.hackathon_assistant.use_cases.get_schedule import GetScheduleUseCase


class TestGetScheduleUseCase:
    """Тесты для GetScheduleUseCase."""

    @pytest.mark.asyncio
    async def test_execute_with_events(self, mock_user_repo, mock_event_repo, sample_user, sample_event):
        """Тест получения расписания с событиями."""
        mock_user_repo.get_by_telegram_id.return_value = sample_user
        mock_event_repo.get_by_hackathon.return_value = [sample_event]

        use_case = GetScheduleUseCase(
            user_repo=mock_user_repo,
            event_repo=mock_event_repo
        )
        telegram_id = 123456789

        result = await use_case.execute(telegram_id)

        mock_user_repo.get_by_telegram_id.assert_called_once_with(telegram_id)
        mock_event_repo.get_by_hackathon.assert_called_once_with(sample_user.current_hackathon_id)
        assert len(result) == 1
        assert result[0].title == sample_event.title
        assert result[0].starts_at == sample_event.starts_at
        assert result[0].ends_at == sample_event.ends_at
        assert result[0].location == sample_event.location

    @pytest.mark.asyncio
    async def test_execute_no_user(self, mock_user_repo, mock_event_repo):
        """Тест получения расписания для несуществующего пользователя."""
        mock_user_repo.get_by_telegram_id.return_value = None

        use_case = GetScheduleUseCase(
            user_repo=mock_user_repo,
            event_repo=mock_event_repo
        )
        telegram_id = 999999999

        result = await use_case.execute(telegram_id)

        mock_user_repo.get_by_telegram_id.assert_called_once_with(telegram_id)
        mock_event_repo.get_by_hackathon.assert_not_called()
        assert result == []

    @pytest.mark.asyncio
    async def test_execute_no_hackathon(self, mock_user_repo, mock_event_repo, sample_user):
        """Тест получения расписания для пользователя без выбранного хакатона."""
        sample_user.current_hackathon_id = None
        mock_user_repo.get_by_telegram_id.return_value = sample_user

        use_case = GetScheduleUseCase(
            user_repo=mock_user_repo,
            event_repo=mock_event_repo
        )
        telegram_id = 123456789

        result = await use_case.execute(telegram_id)

        mock_user_repo.get_by_telegram_id.assert_called_once_with(telegram_id)
        mock_event_repo.get_by_hackathon.assert_not_called()
        assert result == []

    @pytest.mark.asyncio
    async def test_execute_sorted_events(self, mock_user_repo, mock_event_repo, sample_user):
        """Тест сортировки событий по времени начала."""
        now = datetime.now(timezone.utc)
        event1 = sample_user.copy()
        event1.id = 1
        event1.starts_at = now + timedelta(hours=3)
        event2 = sample_user.copy()
        event2.id = 2
        event2.starts_at = now + timedelta(hours=1)
        event3 = sample_user.copy()
        event3.id = 3
        event3.starts_at = now + timedelta(hours=2)

        mock_user_repo.get_by_telegram_id.return_value = sample_user
        mock_event_repo.get_by_hackathon.return_value = [event1, event2, event3]

        use_case = GetScheduleUseCase(
            user_repo=mock_user_repo,
            event_repo=mock_event_repo
        )

        result = await use_case.execute(sample_user.telegram_id)

        assert len(result) == 3
        assert result[0].id == 2  # Самый ранний
        assert result[1].id == 3  # Второй по времени
        assert result[2].id == 1  # Самый поздний