from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from hackathon_assistant.domain.models import (
    Event,
    EventType,
    FAQItem,
    Hackathon,
    ReminderSubscription,
    Rules,
    User,
    UserRole,
)


@pytest.fixture
def sample_user():
    """Фикстура тестового пользователя"""
    return User(
        id=1,
        telegram_id=123456789,
        username="test_user",
        first_name="Test",
        last_name="User",
        role=UserRole.PARTICIPANT,
        current_hackathon_id=1,
    )


@pytest.fixture
def sample_organizer():
    """Фикстура организатора"""
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
    """Фикстура тестового хакатона"""
    now = datetime.now()
    return Hackathon(
        id=1,
        code="HACK2025",
        name="Test Hackathon 2025",
        description="Тестовый хакатон",
        start_at=now,
        end_at=now + timedelta(days=2),
        is_active=True,
    )


@pytest.fixture
def sample_event():
    """Фикстура тестового события"""
    now = datetime.now()
    return Event(
        id=1,
        hackathon_id=1,
        title="Регистрация",
        type=EventType.REGISTRATION,
        starts_at=now + timedelta(hours=1),
        ends_at=now + timedelta(hours=2),
        location="Главный зал",
        description="Регистрация участников",
    )


@pytest.fixture
def sample_faq_item():
    """Фикстура FAQ"""
    return FAQItem(
        id=1, hackathon_id=1, question="Какой размер команды?", answer="От 2 до 5 человек"
    )


@pytest.fixture
def sample_rules():
    """Фикстура правил"""
    return Rules(id=1, hackathon_id=1, content="1. Уважайте друг друга\n2. Соблюдайте сроки")


@pytest.fixture
def sample_subscription():
    """Фикстура подписки на уведомления"""
    return ReminderSubscription(id=1, user_id=1, hackathon_id=1, enabled=True)


@pytest.fixture
def mock_session():
    """Мок асинхронной сессии SQLAlchemy"""
    session = AsyncMock(spec=AsyncSession)
    session.commit = AsyncMock()
    session.flush = AsyncMock()
    session.refresh = AsyncMock()
    session.execute = AsyncMock()
    session.scalars = AsyncMock()
    session.add = MagicMock()
    return session


@pytest.fixture
def mock_session_factory(mock_session):
    """Фабрика для создания мок сессий"""
    factory = MagicMock()
    factory.return_value = mock_session
    factory.__aenter__ = AsyncMock(return_value=mock_session)
    factory.__aexit__ = AsyncMock(return_value=None)
    return factory


@pytest.fixture
def mock_message():
    """Мок сообщения Telegram"""
    message = MagicMock()
    message.from_user.id = 123456789
    message.from_user.username = "test_user"
    message.from_user.first_name = "Test"
    message.from_user.last_name = "User"
    message.text = "/test"
    message.answer = AsyncMock()
    message.reply = AsyncMock()
    return message


@pytest.fixture
def mock_callback_query():
    """Мок callback query"""
    callback = MagicMock()
    callback.from_user.id = 123456789
    callback.data = "test_data"
    callback.message = MagicMock()
    callback.message.edit_text = AsyncMock()
    callback.answer = AsyncMock()
    return callback


@pytest.fixture
def mock_bot():
    """Мок бота Telegram"""
    bot = MagicMock()
    bot.send_message = AsyncMock()
    return bot


@pytest.fixture
def mock_fsm_context():
    """Мок FSMContext"""
    context = MagicMock()
    context.set_state = AsyncMock()
    context.get_state = AsyncMock(return_value=None)
    context.get_data = AsyncMock(return_value={})
    context.update_data = AsyncMock()
    context.clear = AsyncMock()
    return context


@pytest.fixture
def mock_use_cases():
    """Мок UseCaseProvider"""
    use_cases = MagicMock()

    # Моки методов
    use_cases.start_user.execute = AsyncMock()
    use_cases.get_hackathon_info.execute = AsyncMock()
    use_cases.get_schedule.execute = AsyncMock()
    use_cases.get_rules.execute = AsyncMock()
    use_cases.get_faq.execute = AsyncMock()
    use_cases.subscribe_notifications.execute = AsyncMock()
    use_cases.unsubscribe_notifications.execute = AsyncMock()
    use_cases.list_hackathons.execute = AsyncMock()
    use_cases.select_hackathon_by_code.execute = AsyncMock()
    use_cases.get_admin_stats.execute = AsyncMock()
    use_cases.get_upcoming_events.execute = AsyncMock()

    # Мок репозиториев внутри use cases
    use_cases.start_user.user_repo = MagicMock()
    use_cases.start_user.user_repo.get_by_telegram_id = AsyncMock()

    return use_cases
