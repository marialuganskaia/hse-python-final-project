from datetime import datetime, timedelta

from hackathon_assistant.use_cases.dto import (
    ScheduleItemDTO,
    FAQItemDTO,
    HackathonDTO,
    RulesDTO,
    AdminStatsDTO,
)
from hackathon_assistant.adapters.bot.formatters import (
    format_schedule,
    format_faq,
    format_rules,
    format_hackathon_info,
    format_admin_stats,
    format_broadcast_result,
    format_notification_status,
    format_welcome_message,
    format_help_message,
    format_broadcast_preview,
    format_reminder_message
)


class TestFormatters:
    """Тесты функций форматирования"""

    def test_format_schedule_with_items(self):
        """Тест форматирования расписания"""
        now = datetime.now()
        items = [
            ScheduleItemDTO(
                title="Регистрация",
                starts_at=now,
                ends_at=now + timedelta(hours=1),
                location="Холл",
                description="Регистрация участников"
            ),
            ScheduleItemDTO(
                title="Открытие",
                starts_at=now + timedelta(hours=2),
                ends_at=now + timedelta(hours=3),
                location="Аудитория 101",
                description="Торжественное открытие"
            )
        ]

        result = format_schedule(items)

        assert "📅 *Расписание:*" in result
        assert "Регистрация" in result
        assert "Открытие" in result
        assert "Холл" in result
        assert "Аудитория 101" in result

    def test_format_schedule_empty(self):
        """Тест форматирования пустого расписания"""
        result = format_schedule([])

        assert "Расписание пока не добавлено" in result

    def test_format_faq_with_items(self):
        """Тест форматирования FAQ"""
        items = [
            FAQItemDTO(
                question="Какой размер команды?",
                answer="От 2 до 5 человек"
            ),
            FAQItemDTO(
                question="Можно ли участвовать онлайн?",
                answer="Да, есть онлайн-трек"
            )
        ]

        result = format_faq(items)

        assert "❓ *Часто задаваемые вопросы:*" in result
        assert "Какой размер команды?" in result
        assert "От 2 до 5 человек" in result
        assert "Можно ли участвовать онлайн?" in result

    def test_format_faq_empty(self):
        """Тест форматирования пустого FAQ"""
        result = format_faq([])

        assert "FAQ пока не добавлен" in result

    def test_format_rules_with_content(self):
        """Тест форматирования правил"""
        rules = RulesDTO(
            content="1. Уважайте других\n2. Соблюдайте сроки\n3. Веселитесь!"
        )

        result = format_rules(rules)

        assert "📋 *Правила хакатона:*" in result
        assert "Уважайте других" in result
        assert "Соблюдайте сроки" in result

    def test_format_rules_none(self):
        """Тест форматирования отсутствующих правил"""
        result = format_rules(None)

        assert "Правила пока не добавлены" in result
        assert "Основные правила:" in result

    def test_format_hackathon_info(self):
        """Тест форматирования информации о хакатоне"""
        now = datetime.now()
        hackathon = HackathonDTO(
            id=1,
            code="HACK2024",
            name="Тестовый хакатон",
            description="Описание хакатона",
            start_at=now,
            end_at=now + timedelta(days=2),
            is_active=True,
            location="Москва"
        )

        result_subscribed = format_hackathon_info(hackathon, True)
        result_not_subscribed = format_hackathon_info(hackathon, False)

        assert "🏆 *Тестовый хакатон*" in result_subscribed
        assert "HACK2024" in result_subscribed
        assert "Описание хакатона" in result_subscribed
        assert "Москва" in result_subscribed
        assert "✅ Включены" in result_subscribed
        assert "❌ Выключены" in result_not_subscribed

    def test_format_admin_stats(self):
        """Тест форматирования статистики администратора"""
        stats = AdminStatsDTO(
            total_users=100,
            participants=85,
            organizers=15,
            subscribed_users=60
        )

        result = format_admin_stats(stats)

        assert "Всего пользователей: 100" in result
        assert "Участников: 85" in result
        assert "Организаторов: 15" in result
        assert "Подписаны на напоминания: 60" in result

    def test_format_broadcast_result(self):
        """Тест форматирования результата рассылки"""
        result = format_broadcast_result(sent=95, failed=5, total=100)

        assert "📨 *Результат рассылки:*" in result
        assert "✅ Успешно: 95" in result
        assert "❌ Ошибки: 5" in result
        assert "📊 Всего: 100" in result
        assert "📈 Успешность: 95.0%" in result

    def test_format_notification_status(self):
        """Тест форматирования статуса уведомлений"""
        enabled_result = format_notification_status(True)
        disabled_result = format_notification_status(False)

        assert "✅ Уведомления включены!" in enabled_result
        assert "🔕 Уведомления выключены" in disabled_result

    def test_format_welcome_message(self):
        """Тест форматирования приветственного сообщения"""
        result_with_name = format_welcome_message("TestUser")
        result_without_name = format_welcome_message()

        assert "👋 Привет, TestUser!" in result_with_name
        assert "👋 Привет, друг!" in result_without_name
        assert "бот для участников хакатона" in result_with_name

    def test_format_help_message(self):
        """Тест форматирования справочного сообщения"""
        result = format_help_message([])

        assert "ℹ️ *Доступные команды:*" in result
        assert "/start" in result
        assert "/help" in result
        assert "/schedule" in result
        assert "/rules" in result
        assert "/faq" in result
        assert "📌 *Как начать:*" in result

    def test_format_broadcast_preview(self):
        """Тест форматирования предпросмотра рассылки"""
        hackathon_name = "Тестовый хакатон"
        user_count = 150
        message = "Важное сообщение для всех участников!"

        result = format_broadcast_preview(hackathon_name, user_count, message)

        assert "📨 *Предпросмотр рассылки:*" in result
        assert "Тестовый хакатон" in result
        assert "150" in result
        assert "Важное сообщение" in result
        assert "Подтвердите отправку:" in result

    def test_format_reminder_message(self):
        """Тест форматирования напоминания"""

        class MockEvent:
            title = "Регистрация"
            starts_at = datetime.now() + timedelta(minutes=30)
            location = "Главный зал"
            description = "Регистрация участников хакатона"

        event = MockEvent()

        result = format_reminder_message(event, 30)

        assert "🔔 *Напоминание*" in result
        assert "Через *30 минут*" in result
        assert "*Регистрация*" in result
        assert "Главный зал" in result
        assert "Регистрация участников" in result
