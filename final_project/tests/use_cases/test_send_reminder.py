from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from hackathon_assistant.use_cases.dto import (
    ReminderEventDTO,
    ReminderParticipantDTO,
    ReminderPileDTO,
)


class TestSendRemindersUseCase:
    """Тесты для SendRemindersUseCase"""

    @pytest.mark.asyncio
    async def test_send_reminders_single_pile(
        self, use_case_send_reminder, mock_notifier, sample_pile
    ):
        """Отправка напоминаний для одного события с несколькими участниками"""
        piles = [sample_pile]

        await use_case_send_reminder.execute(piles)

        assert mock_notifier.send.call_count == 2

        first_call = mock_notifier.send.call_args_list[0]
        assert first_call.kwargs["telegram_id"] == 111
        assert "Тестовое событие" in first_call.kwargs["text"]
        assert "🕐" in first_call.kwargs["text"]

        second_call = mock_notifier.send.call_args_list[1]
        assert second_call.kwargs["telegram_id"] == 222

    @pytest.mark.asyncio
    async def test_send_reminders_multiple_piles(self, use_case_send_reminder, mock_notifier):
        """Отправка напоминаний для нескольких событий"""
        now = datetime.now()

        piles = [
            ReminderPileDTO(
                event=ReminderEventDTO(
                    event_id=1, title="Событие 1", starts_at=now + timedelta(hours=1)
                ),
                participants=[ReminderParticipantDTO(user_id=1, telegram_id=111)],
            ),
            ReminderPileDTO(
                event=ReminderEventDTO(
                    event_id=2, title="Событие 2", starts_at=now + timedelta(hours=2)
                ),
                participants=[ReminderParticipantDTO(user_id=2, telegram_id=222)],
            ),
        ]

        await use_case_send_reminder.execute(piles)

        assert mock_notifier.send.call_count == 2

        first_call = mock_notifier.send.call_args_list[0]
        assert "Событие 1" in first_call.kwargs["text"]

        second_call = mock_notifier.send.call_args_list[1]
        assert "Событие 2" in second_call.kwargs["text"]

    @pytest.mark.asyncio
    async def test_send_reminders_empty_piles(self, use_case_send_reminder, mock_notifier):
        """Пустой список напоминаний"""
        await use_case_send_reminder.execute([])

        mock_notifier.send.assert_not_called()

    @pytest.mark.asyncio
    async def test_send_reminders_pile_without_participants(
        self, use_case_send_reminder, mock_notifier
    ):
        """Событие без участников"""
        pile = ReminderPileDTO(
            event=ReminderEventDTO(event_id=1, title="Событие", starts_at=datetime.now()),
            participants=[],
        )

        await use_case_send_reminder.execute([pile])

        mock_notifier.send.assert_not_called()

    @pytest.mark.asyncio
    async def test_send_reminders_message_format(self, use_case_send_reminder, mock_notifier):
        """Проверка формата сообщения"""
        now = datetime.now(UTC)
        pile = ReminderPileDTO(
            event=ReminderEventDTO(event_id=1, title="Важное собрание", starts_at=now),
            participants=[ReminderParticipantDTO(user_id=1, telegram_id=123)],
        )

        await use_case_send_reminder.execute([pile])

        mock_notifier.send.assert_called_once()
        call = mock_notifier.send.call_args

        text = call.kwargs["text"]
        assert "Скоро событие" in text
        assert "Важное собрание" in text
        assert "🕐" in text
        assert now.astimezone(ZoneInfo("Europe/Moscow")).strftime("%H:%M") in text
