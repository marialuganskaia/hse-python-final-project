from __future__ import annotations

from typing import Any

from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

import pytest

from final_project.src.hackathon_assistant.domain.models import (
    Event,
    EventType,
    FAQItem,
    Hackathon,
    ReminderSubscription,
    Rules,
    User,
    UserRole,
)
from final_project.src.hackathon_assistant.use_cases.get_admin_stats import GetAdminStatsUseCase
from final_project.src.hackathon_assistant.use_cases.send_broadcast import SendBroadcastUseCase
from final_project.src.hackathon_assistant.use_cases.finish_hackathon import FinishHackathonUseCase
from final_project.src.hackathon_assistant.use_cases.get_hackathon_info import GetHackathonInfoUseCase
from final_project.src.hackathon_assistant.use_cases.create_hackathon import CreateHackathonFromConfigUseCase
from final_project.src.hackathon_assistant.use_cases.process_reminder import ProcessRemindersUseCase
from final_project.src.hackathon_assistant.use_cases.send_reminder import SendRemindersUseCase
from final_project.src.hackathon_assistant.use_cases.dto import (
    ReminderPileDTO, ReminderEventDTO, ReminderParticipantDTO
)


@pytest.fixture
def mock_user_repo():
    """Фикстура мока UserRepository."""
    return AsyncMock()


@pytest.fixture
def mock_hackathon_repo():
    """Фикстура мока HackathonRepository."""
    return AsyncMock()


@pytest.fixture
def mock_event_repo():
    """Фикстура мока EventRepository."""
    return AsyncMock()


@pytest.fixture
def mock_faq_repo():
    """Фикстура мока FAQRepository."""
    return AsyncMock()


@pytest.fixture
def mock_rules_repo():
    """Фикстура мока RulesRepository."""
    return AsyncMock()


@pytest.fixture
def mock_subscription_repo():
    """Фикстура мока SubscriptionRepository."""
    return AsyncMock()

@pytest.fixture
def mock_notifier():
    return AsyncMock()


@pytest.fixture
def sample_user():
    """Пример пользователя для тестов."""
    return User(
        id=1,
        telegram_id=123456789,
        username="testuser",
        first_name="Test",
        last_name="User",
        role=UserRole.PARTICIPANT,
        current_hackathon_id=1,
    )


@pytest.fixture
def sample_organizer():
    """Пример организатора для тестов."""
    return User(
        id=2,
        telegram_id=987654321,
        username="organizer",
        first_name="Organizer",
        last_name="Admin",
        role=UserRole.ORGANIZER,
        current_hackathon_id=1,
    )


@pytest.fixture
def sample_hackathon():
    """Пример хакатона для тестов."""
    now = datetime.now(UTC)
    return Hackathon(
        id=1,
        code="HACK2024",
        name="Test Hackathon",
        description="Test description",
        start_at=now,
        end_at=now + timedelta(days=3),
        is_active=True,
        location="Test Location"
    )


@pytest.fixture
def sample_event():
    """Пример события для тестов."""
    now = datetime.now(UTC)
    return Event(
        id=1,
        hackathon_id=1,
        title="Test Event",
        type=EventType.LECTURE,
        starts_at=now + timedelta(hours=1),
        ends_at=now + timedelta(hours=2),
        location="Test Location",
        description="Test Description",
    )


@pytest.fixture
def sample_faq_item():
    """Пример FAQ для тестов."""
    return FAQItem(
        id=1,
        hackathon_id=1,
        question="Test Question?",
        answer="Test Answer.",
    )


@pytest.fixture
def sample_rules():
    """Пример правил для тестов."""
    return Rules(
        id=1,
        hackathon_id=1,
        content="1. Test Rule\n2. Another Rule",
    )


@pytest.fixture
def sample_subscription():
    """Пример подписки для тестов."""
    return ReminderSubscription(
        id=1,
        user_id=1,
        hackathon_id=1,
        enabled=True,
    )

@pytest.fixture
def use_case_admin_stats(mock_user_repo, mock_subscription_repo, mock_hackathon_repo):
    return GetAdminStatsUseCase(
        user_repo=mock_user_repo,
        subscription_repo=mock_subscription_repo,
        hackathon_repo=mock_hackathon_repo
    )

@pytest.fixture
def use_case_send_broadcast(mock_user_repo, mock_subscription_repo):
    return SendBroadcastUseCase(
        user_repo=mock_user_repo,
        subscription_repo=mock_subscription_repo
    )

@pytest.fixture
def use_case_finish_hackathon(mock_hackathon_repo, mock_subscription_repo):
    return FinishHackathonUseCase(
        hackathon_repo=mock_hackathon_repo,
        subscription_repo=mock_subscription_repo
    )

@pytest.fixture
def use_case_get_hackathon_info(mock_user_repo, mock_hackathon_repo, mock_subscription_repo):
    return GetHackathonInfoUseCase(
        user_repo=mock_user_repo,
        hackathon_repo=mock_hackathon_repo,
        subscription_repo=mock_subscription_repo
    )

@pytest.fixture
def use_case_create_hackathon(mock_hackathon_repo, mock_event_repo, mock_faq_repo, mock_rules_repo):
    return CreateHackathonFromConfigUseCase(
        hackathon_repo=mock_hackathon_repo,
        event_repo=mock_event_repo,
        faq_repo=mock_faq_repo,
        rules_repo=mock_rules_repo
    )

@pytest.fixture
def sample_config() -> dict[str, Any]:
    """Пример конфига для тестов"""
    now = datetime.now()
    return {
        "name": "Test Hackathon 2024",
        "code": "TEST2024",
        "description": "Test description",
        "start_at": now,
        "end_at": now + timedelta(days=2),
        "is_active": True,
        "events": [
            {
                "title": "Opening Ceremony",
                "type": EventType.OTHER,
                "starts_at": now,
                "ends_at": now + timedelta(hours=1),
                "location": "Main Hall",
                "description": "Welcome speech"
            },
            {
                "title": "Workshop",
                "type": EventType.LECTURE,
                "starts_at": now + timedelta(hours=2),
                "ends_at": now + timedelta(hours=3),
                "location": "Room 101",
                "description": "Python workshop"
            }
        ],
        "rules": {
            "content": "1. Be respectful\n2. No cheating\n3. Have fun!"
        },
        "faq": [
            {
                "question": "What is the team size?",
                "answer": "2-5 people per team"
            },
            {
                "question": "Is food provided?",
                "answer": "Yes, meals and snacks will be provided"
            }
        ]
    }

@pytest.fixture
def use_case_process_reminder(mock_event_repo, mock_subscription_repo):
    return ProcessRemindersUseCase(
        event_repo=mock_event_repo,
        subscription_repo=mock_subscription_repo
    )

@pytest.fixture
def use_case_send_reminder(mock_notifier):
    return SendRemindersUseCase(notifier=mock_notifier)

@pytest.fixture
def sample_pile():
    """Пример ReminderPileDTO для тестов"""
    return ReminderPileDTO(
        event=ReminderEventDTO(
            event_id=1,
            title="Тестовое событие",
            starts_at=datetime.now() + timedelta(minutes=30)
        ),
        participants=[
            ReminderParticipantDTO(user_id=1, telegram_id=111),
            ReminderParticipantDTO(user_id=2, telegram_id=222)
        ]
    )