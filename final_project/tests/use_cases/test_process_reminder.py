from datetime import datetime, timedelta

import pytest

from hackathon_assistant.domain.models import Event, EventType, User, UserRole
from hackathon_assistant.use_cases.dto import ReminderPileDTO


class TestProcessRemindersUseCase:
    """Тесты для ProcessRemindersUseCase"""

    @pytest.mark.asyncio
    async def test_process_reminders_with_data(
        self, use_case_process_reminder, mock_event_repo, mock_subscription_repo
    ):
        """Обработка напоминаний с событиями и пользователями"""
        now = datetime.now()
        events = [
            Event(
                id=1,
                hackathon_id=1,
                title="Test Event",
                type=EventType.CHECKPOINT,
                starts_at=now + timedelta(minutes=30),
                ends_at=now + timedelta(hours=1),
            )
        ]

        users = [
            User(id=1, telegram_id=111, username="user1", role=UserRole.PARTICIPANT),
            User(id=2, telegram_id=222, username="user2", role=UserRole.PARTICIPANT),
        ]

        mock_event_repo.get_upcoming_events.return_value = events
        mock_subscription_repo.get_subscribed_users.return_value = users

        result = await use_case_process_reminder.execute(hackathon_id=1, hours_ahead=1)

        mock_event_repo.get_upcoming_events.assert_called_once_with(hackathon_id=1, hours_ahead=1)
        mock_subscription_repo.get_subscribed_users.assert_called_once_with(1)

        assert len(result) == 1
        pile = result[0]
        assert isinstance(pile, ReminderPileDTO)
        assert pile.event.event_id == 1
        assert pile.event.title == "Test Event"
        assert len(pile.participants) == 2
        assert pile.participants[0].user_id == 1
        assert pile.participants[0].telegram_id == 111
        assert pile.participants[1].user_id == 2
        assert pile.participants[1].telegram_id == 222

    @pytest.mark.asyncio
    async def test_process_reminders_no_events(
        self, use_case_process_reminder, mock_event_repo, mock_subscription_repo
    ):
        """Нет событий для напоминаний"""
        mock_event_repo.get_upcoming_events.return_value = []

        result = await use_case_process_reminder.execute(hackathon_id=1)

        mock_event_repo.get_upcoming_events.assert_called_once()
        mock_subscription_repo.get_subscribed_users.assert_not_called()
        assert result == []

    @pytest.mark.asyncio
    async def test_process_reminders_no_users(
        self, use_case_process_reminder, mock_event_repo, mock_subscription_repo
    ):
        """Нет подписанных пользователей"""
        now = datetime.now()
        events = [
            Event(
                id=1,
                hackathon_id=1,
                title="Event",
                type=EventType.OTHER,
                starts_at=now + timedelta(minutes=30),
                ends_at=now + timedelta(hours=1),
            )
        ]

        mock_event_repo.get_upcoming_events.return_value = events
        mock_subscription_repo.get_subscribed_users.return_value = []

        result = await use_case_process_reminder.execute(hackathon_id=1)

        mock_event_repo.get_upcoming_events.assert_called_once()
        mock_subscription_repo.get_subscribed_users.assert_called_once()
        assert result == []

    @pytest.mark.asyncio
    async def test_process_reminders_multiple_events_same_users(
        self, use_case_process_reminder, mock_event_repo, mock_subscription_repo
    ):
        """Несколько событий для одних и тех же пользователей"""
        now = datetime.now()
        events = [
            Event(
                id=1,
                hackathon_id=1,
                title="Event 1",
                type=EventType.CHECKPOINT,
                starts_at=now + timedelta(minutes=30),
                ends_at=now + timedelta(hours=1),
            ),
            Event(
                id=2,
                hackathon_id=1,
                title="Event 2",
                type=EventType.LECTURE,
                starts_at=now + timedelta(hours=2),
                ends_at=now + timedelta(hours=3),
            ),
        ]

        users = [User(id=1, telegram_id=111, username="user1", role=UserRole.PARTICIPANT)]

        mock_event_repo.get_upcoming_events.return_value = events
        mock_subscription_repo.get_subscribed_users.return_value = users

        result = await use_case_process_reminder.execute(hackathon_id=1)

        assert len(result) == 2
        assert result[0].event.event_id == 1
        assert result[0].event.title == "Event 1"
        assert result[1].event.event_id == 2
        assert result[1].event.title == "Event 2"
        assert len(result[0].participants) == 1
        assert len(result[1].participants) == 1
        assert result[0].participants[0].user_id == result[1].participants[0].user_id == 1
