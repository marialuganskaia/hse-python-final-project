from datetime import UTC, datetime, timedelta

import pytest

from final_project.src.hackathon_assistant.domain.models import EventType, UserRole


@pytest.fixture
def sample_datetime():
    """Фикстура с тестовым datetime."""
    return datetime(2025, 12, 4, 10, 0, 0, tzinfo=UTC)


@pytest.fixture
def sample_user_data():
    """Тестовые данные для пользователя."""
    return {
        "telegram_id": 123456789,
        "username": "test_user",
        "first_name": "Test",
        "last_name": "User",
        "role": UserRole.PARTICIPANT,
        "current_hackathon_id": 1,
    }


@pytest.fixture
def sample_hackathon_data(sample_datetime):
    """Тестовые данные для хакатона."""
    return {
        "code": "HACK2025",
        "name": "Тестовый Хакатон",
        "description": "Описание тестового хакатона",
        "start_at": sample_datetime,
        "end_at": sample_datetime + timedelta(days=3),
        "is_active": True,
    }


@pytest.fixture
def sample_event_data(sample_datetime):
    """Тестовые данные для события."""
    return {
        "hackathon_id": 1,
        "title": "Чекпоинт #1",
        "type": EventType.CHECKPOINT,
        "starts_at": sample_datetime + timedelta(hours=2),
        "ends_at": sample_datetime + timedelta(hours=3),
        "location": "Зал А",
        "description": "Промежуточная сдача прототипа",
    }


@pytest.fixture
def sample_faq_data():
    """Тестовые данные для FAQ."""
    return {"hackathon_id": 1, "question": "Question?", "answer": "Answer.", "id": 123}


@pytest.fixture
def sample_rules_data():
    """Тестовые данные для правил."""
    return {"hackathon_id": 1, "content": "1. Правило\n2. Еще правило", "id": 123}


@pytest.fixture
def sample_reminder_subscription_data():
    """Тестовые данные для правил."""
    return {"user_id": 123456789, "hackathon_id": 1, "id": 123, "enabled": True}
