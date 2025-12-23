from hackathon_assistant.domain.models import EventType, UserRole


class TestUserRole:
    def test_user_role_values(self):
        """Проверка всех возможных значений ролей."""
        expected = ["participant", "organizer"]
        assert list(UserRole) == expected

    def test_user_role_enum(self):
        """Проверка корректности Enum."""
        assert UserRole.PARTICIPANT == "participant"
        assert UserRole.ORGANIZER == "organizer"


class TestEventType:
    def test_event_type_values(self):
        """Проверка всех возможных типов событий."""
        expected = ["checkpoint", "deadline", "meetup", "lecture", "other"]
        assert list(EventType) == expected

    def test_event_type_enum(self):
        """Проверка корректности Enum."""
        assert EventType.CHECKPOINT == "checkpoint"
        assert EventType.DEADLINE == "deadline"
        assert EventType.MEETUP == "meetup"
        assert EventType.LECTURE == "lecture"
        assert EventType.OTHER == "other"
