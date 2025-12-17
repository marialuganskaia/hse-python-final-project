from dataclasses import is_dataclass
from datetime import timedelta

import pytest
from src.hackathon_assistant.domain.models import (
    Event,
    EventType,
    FAQItem,
    Hackathon,
    ReminderSubscription,
    Rules,
    User,
    UserRole,
)


class TestUser:
    """Тесты для сущности User."""

    def test_user_is_dataclass(self):
        """Проверка, что User является dataclass."""
        assert is_dataclass(User)

    def test_user_creation_with_all_data(self, sample_user_data):
        """Создание пользователя со всеми данными."""
        user = User(**sample_user_data)

        assert user.telegram_id == 123456789
        assert user.username == "test_user"
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.role == UserRole.PARTICIPANT
        assert user.current_hackathon_id == 1

    def test_user_role_validation_invalid(self, sample_user_data):
        """Валидация некорректной роли должна вызывать ошибку."""
        with pytest.raises(ValueError, match="Роль должна быть одной из:"):
            data = sample_user_data.copy()
            data["role"] = "invalid_role"
            User(**data)

    def test_user_telegram_id_validation(self, sample_user_data):
        """Валидация telegram_id."""
        # Некорректный telegram_id (не число)
        with pytest.raises(ValueError, match="telegram_id должен быть положительным числом"):
            data = sample_user_data.copy()
            data["telegram_id"] = "not_a_number"
            User(**data)

        # Некорректный telegram_id (отрицательный)
        with pytest.raises(ValueError, match="telegram_id должен быть положительным числом"):
            data = sample_user_data.copy()
            data["telegram_id"] = -123
            User(**data)

        # Некорректный telegram_id (ноль)
        with pytest.raises(ValueError, match="telegram_id должен быть положительным числом"):
            data = sample_user_data.copy()
            data["telegram_id"] = 0
            User(**data)

    def test_user_is_organizer_method(self, sample_user_data):
        """Тест метода is_organizer()."""
        participant = User(**sample_user_data)
        data = sample_user_data.copy()
        data["role"] = UserRole.ORGANIZER
        organizer = User(**data)

        assert participant.is_organizer() is False
        assert organizer.is_organizer() is True


class TestHackathon:
    """Тесты для сущности Hackathon."""

    def test_hackathon_is_dataclass(self):
        """Проверка, что Hackathon является dataclass."""
        assert is_dataclass(Hackathon)

    def test_hackathon_creation_with_all_data(self, sample_hackathon_data):
        """Создание хакатона со всеми данными."""
        hackathon = Hackathon(**sample_hackathon_data)

        assert hackathon.code == "HACK2025"
        assert hackathon.name == "Тестовый Хакатон"
        assert hackathon.description == "Описание тестового хакатона"
        assert hackathon.is_active is True

    def test_hackathon_code_validation(self, sample_hackathon_data):
        """Валидация кода хакатона."""
        # Пустой код
        with pytest.raises(ValueError, match="Код хакатона не может быть пустым"):
            data = sample_hackathon_data.copy()
            data["code"] = ""
            Hackathon(**data)

        # Код только из пробелов
        with pytest.raises(ValueError, match="Код хакатона не может быть пустым"):
            data = sample_hackathon_data.copy()
            data["code"] = "   "
            Hackathon(**data)

    def test_hackathon_name_validation(self, sample_hackathon_data):
        """Валидация названия хакатона."""
        # Пустое название
        with pytest.raises(ValueError, match="Название хакатона не может быть пустым"):
            data = sample_hackathon_data.copy()
            data["name"] = ""
            Hackathon(**data)

    def test_hackathon_dates_validation(self, sample_datetime, sample_hackathon_data):
        """Валидация дат хакатона."""
        # Начало позже окончания
        with pytest.raises(ValueError, match="Дата начала должна быть раньше даты окончания"):
            data = sample_hackathon_data.copy()
            data["start_at"] = sample_datetime + timedelta(days=2)
            data["end_at"] = sample_datetime
            Hackathon(**data)

        # Начало равно окончанию
        with pytest.raises(ValueError, match="Дата начала должна быть раньше даты окончания"):
            data = sample_hackathon_data.copy()
            data["start_at"] = sample_datetime
            data["end_at"] = sample_datetime
            Hackathon(**data)


class TestEvent:
    """Тесты для сущности Event."""

    def test_event_is_dataclass(self):
        """Проверка, что Event является dataclass."""
        assert is_dataclass(Event)

    def test_event_creation_with_all_data(self, sample_event_data):
        """Создание события со всеми данными."""
        event = Event(**sample_event_data)

        assert event.hackathon_id == 1
        assert event.title == "Чекпоинт #1"
        assert event.type == EventType.CHECKPOINT
        assert event.location == "Зал А"
        assert event.description == "Промежуточная сдача прототипа"

    def test_event_title_validation(self, sample_event_data):
        """Валидация названия события."""
        # Пустой заголовок
        with pytest.raises(ValueError, match="Название события не может быть пустым"):
            data = sample_event_data.copy()
            data["title"] = ""
            Event(**data)

        # Заголовок только из пробелов
        with pytest.raises(ValueError, match="Название события не может быть пустым"):
            data = sample_event_data.copy()
            data["title"] = "   "
            Event(**data)

    def test_event_dates_validation(self, sample_datetime, sample_event_data):
        """Валидация дат события."""
        # Начало позже окончания
        with pytest.raises(ValueError, match="Начало события должно быть раньше окончания"):
            data = sample_event_data.copy()
            data["start_at"] = sample_datetime + timedelta(hours=2)
            data["end_at"] = sample_datetime
            Event(**data)

        # Начало равно окончанию
        with pytest.raises(ValueError, match="Начало события должно быть раньше окончания"):
            data = sample_event_data.copy()
            data["start_at"] = sample_datetime
            data["end_at"] = sample_datetime
            Event(**data)

    def test_event_type_validation(self, sample_event_data):
        """Валидация типа события."""
        # Некорректный тип
        with pytest.raises(ValueError, match="Тип события должен быть одним из:"):
            data = sample_event_data.copy()
            data["type"] = "invalid_type"
            Event(**data)


class TestFAQItem:
    """Тесты для сущности FAQItem."""

    def test_faq_is_dataclass(self):
        """Проверка, что FAQItem является dataclass."""
        assert is_dataclass(FAQItem)

    def test_faq_creation(self, sample_faq_data):
        """Создание FAQ."""
        faq = FAQItem(**sample_faq_data)

        assert faq.hackathon_id == 1
        assert faq.question == "Question?"
        assert faq.answer == "Answer."
        assert faq.id == 123

    def test_faq_question_validation(self, sample_faq_data):
        """Валидация вопроса FAQ."""
        # Пустой вопрос
        with pytest.raises(ValueError, match="Вопрос не может быть пустым"):
            data = sample_faq_data.copy()
            data["question"] = ""
            FAQItem(**data)

        # Вопрос только из пробелов
        with pytest.raises(ValueError, match="Вопрос не может быть пустым"):
            data = sample_faq_data.copy()
            data["question"] = "   "
            FAQItem(**data)

    def test_faq_answer_validation(self, sample_faq_data):
        """Валидация ответа FAQ."""
        # Пустой ответ
        with pytest.raises(ValueError, match="Ответ не может быть пустым"):
            data = sample_faq_data.copy()
            data["answer"] = ""
            FAQItem(**data)


class TestRules:
    """Тесты для сущности Rules."""

    def test_rules_is_dataclass(self):
        """Проверка, что Rules является dataclass."""
        assert is_dataclass(Rules)

    def test_rules_creation(self, sample_rules_data):
        """Создание правил."""
        rules = Rules(**sample_rules_data)

        assert rules.hackathon_id == 1
        assert rules.content == "1. Правило\n2. Еще правило"
        assert rules.id == 123

    def test_rules_content_validation(self, sample_rules_data):
        """Валидация содержания правил."""
        # Пустой контент
        with pytest.raises(ValueError, match="Текст правил не может быть пустым"):
            data = sample_rules_data.copy()
            data["content"] = ""
            Rules(**data)

        # Контент только из пробелов
        with pytest.raises(ValueError, match="Текст правил не может быть пустым"):
            data = sample_rules_data.copy()
            data["content"] = "   "
            Rules(**data)


class TestReminderSubscription:
    """Тесты для сущности ReminderSubscription."""

    def test_subscription_is_dataclass(self):
        """Проверка, что ReminderSubscription является dataclass."""
        assert is_dataclass(ReminderSubscription)

    def test_subscription_creation_with_all_data(self, sample_reminder_subscription_data):
        """Создание подписки."""
        subscription = ReminderSubscription(**sample_reminder_subscription_data)

        assert subscription.user_id == 123456789
        assert subscription.hackathon_id == 1
        assert subscription.enabled is True
        assert subscription.id == 123

    def test_subscription_creation_disabled(self, sample_reminder_subscription_data):
        """Создание отключенной подписки."""
        data = sample_reminder_subscription_data.copy()
        data["enabled"] = False
        subscription = ReminderSubscription(**data)

        assert subscription.enabled is False

    def test_subscription_user_id_validation(self, sample_reminder_subscription_data):
        """Валидация user_id."""
        # Некорректный user_id
        with pytest.raises(ValueError, match="ID пользователя должен быть положительным числом"):
            data = sample_reminder_subscription_data.copy()
            data["user_id"] = 0
            ReminderSubscription(**data)

        with pytest.raises(ValueError, match="ID пользователя должен быть положительным числом"):
            data = sample_reminder_subscription_data.copy()
            data["user_id"] = -1
            ReminderSubscription(**data)

    def test_subscription_hackathon_id_validation(self, sample_reminder_subscription_data):
        """Валидация hackathon_id."""
        # Некорректный hackathon_id
        with pytest.raises(ValueError, match="ID хакатона должен быть положительным числом"):
            data = sample_reminder_subscription_data.copy()
            data["hackathon_id"] = 0
            ReminderSubscription(**data)

        with pytest.raises(ValueError, match="ID хакатона должен быть положительным числом"):
            data = sample_reminder_subscription_data.copy()
            data["hackathon_id"] = -1
            ReminderSubscription(**data)
