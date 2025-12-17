from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock

import pytest

from final_project.src.hackathon_assistant.domain.models import (
    User, Hackathon, Event, FAQItem, Rules, ReminderSubscription,
    UserRole, EventType
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
    now = datetime.now(timezone.utc)
    return Hackathon(
        id=1,
        code="HACK2024",
        name="Test Hackathon",
        description="Test description",
        start_at=now,
        end_at=now + timedelta(days=3),
        is_active=True,
    )


@pytest.fixture
def sample_event():
    """Пример события для тестов."""
    now = datetime.now(timezone.utc)
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