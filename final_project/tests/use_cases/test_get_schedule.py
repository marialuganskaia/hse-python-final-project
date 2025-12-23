from datetime import UTC, datetime, timedelta

import pytest

from final_project.src.hackathon_assistant.domain.models import Event, EventType
from final_project.src.hackathon_assistant.use_cases.get_schedule import GetScheduleUseCase


class TestGetScheduleUseCase:
    """Тесты для GetScheduleUseCase."""

    @pytest.mark.asyncio
    async def test_execute_with_events(
        self, mock_user_repo, mock_event_repo, sample_user, sample_event
    ):
        """Тест получения расписания с событиями."""
        mock_user_repo.get_by_telegram_id.return_value = sample_user
        mock_event_repo.get_by_hackathon.return_value = [sample_event]

        use_case = GetScheduleUseCase(user_repo=mock_user_repo, event_repo=mock_event_repo)
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

        use_case = GetScheduleUseCase(user_repo=mock_user_repo, event_repo=mock_event_repo)
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

        use_case = GetScheduleUseCase(user_repo=mock_user_repo, event_repo=mock_event_repo)
        telegram_id = 123456789

        result = await use_case.execute(telegram_id)

        mock_user_repo.get_by_telegram_id.assert_called_once_with(telegram_id)
        mock_event_repo.get_by_hackathon.assert_not_called()
        assert result == []

    @pytest.mark.asyncio
    async def test_execute_sorted_events(self, mock_user_repo, mock_event_repo, sample_user):
        """Тест сортировки событий по времени начала."""
        mock_user_repo.get_by_telegram_id.return_value = sample_user

        now = datetime.now(UTC)
        e1 = Event(
            id=1,
            hackathon_id=sample_user.current_hackathon_id,
            title="E1",
            type=EventType.OTHER,
            starts_at=now + timedelta(hours=2),
            ends_at=now + timedelta(hours=3),
        )
        e2 = Event(
            id=2,
            hackathon_id=sample_user.current_hackathon_id,
            title="E2",
            type=EventType.OTHER,
            starts_at=now + timedelta(hours=1),
            ends_at=now + timedelta(hours=2),
        )
        mock_event_repo.get_by_hackathon.return_value = [e1, e2]

        use_case = GetScheduleUseCase(user_repo=mock_user_repo, event_repo=mock_event_repo)
        result = await use_case.execute(sample_user.telegram_id)

        assert len(result) == 2
        assert result[0].starts_at <= result[1].starts_at
