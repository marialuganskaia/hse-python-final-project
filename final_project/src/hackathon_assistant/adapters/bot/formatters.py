"""Форматирование ответов бота"""

from hackathon_assistant.use_cases.dto import (
    AdminStatsDTO,
    FAQItemDTO,
    HackathonDTO,
    RulesDTO,
    ScheduleItemDTO,
)


def format_schedule(items: list[ScheduleItemDTO]) -> str:
    if not items:
        return (
            "📅 *Расписание*\n\n"
            "Расписание пока не добавлено организаторами.\n"
            "Следите за обновлениями!"
        )

    items_by_day = {}
    for item in items:
        day_key = item.starts_at.strftime("%d.%m.%Y")
        if day_key not in items_by_day:
            items_by_day[day_key] = []
        items_by_day[day_key].append(item)

    result = "📅 *Расписание:*\n\n"

    for day, day_items in sorted(items_by_day.items()):
        result += f"*📆 {day}:*\n"

        day_items.sort(key=lambda x: x.starts_at)

        for item in day_items:
            time_str = f"{item.starts_at.strftime('%H:%M')}–{item.ends_at.strftime('%H:%M')}"

            result += f"  • *{item.title}* ({time_str})\n"

            if item.location:
                result += f"    📍 {item.location}\n"
            if item.description:
                desc = (
                    item.description[:100] + "..."
                    if len(item.description) > 100
                    else item.description
                )
                result += f"    📝 {desc}\n"

            result += "\n"

    return result


def format_faq(items: list[FAQItemDTO]) -> str:
    if not items:
        return (
            "❓ *Часто задаваемые вопросы*\n\n"
            "FAQ пока не добавлен организаторами.\n"
            "Если у вас есть вопросы, обратитесь к организаторам напрямую."
        )

    result = "❓ *Часто задаваемые вопросы:*\n\n"

    for i, item in enumerate(items, 1):
        result += f"*{i}. {item.question}*\n"
        result += f"{item.answer}\n\n"

    return result


def format_rules(rules: RulesDTO | None) -> str:
    if not rules or not rules.content:
        return (
            "📋 *Правила хакатона*\n\n"
            "Правила пока не добавлены организаторами.\n"
            "Основные правила:\n"
            "• Уважайте других участников\n"
            "• Соблюдайте сроки\n"
            "• Не используйте чужой код\n"
            "• Получайте удовольствие!"
        )

    return f"📋 *Правила хакатона:*\n\n{rules.content}"


def format_hackathon_info(hackathon: HackathonDTO, is_subscribed: bool = False) -> str:
    """
    Форматирование информации о хакатоне

    Args:
        hackathon: информация о хакатоне
        is_subscribed: подписан ли пользователь на уведомления

    Returns:
        Отформатированная информация о хакатоне
    """
    result = f"🏆 *{hackathon.name}*\n\n"

    if hackathon.description:
        result += f"{hackathon.description}\n\n"

    # Даты
    start_date = hackathon.start_at.strftime("%d.%m.%Y %H:%M")
    end_date = hackathon.end_at.strftime("%d.%m.%Y %H:%M")
    result += f"📅 *Даты:* {start_date} – {end_date}\n"

    if hackathon.location:
        result += f"📍 *Место:* {hackathon.location}\n"

    if hackathon.code:
        result += f"🔑 *Код:* `{hackathon.code}`\n"

    # Статус подписки
    subscription_status = "✅ Включены" if is_subscribed else "❌ Выключены"
    result += f"\n🔔 *Уведомления:* {subscription_status}\n"

    return result


def format_admin_stats(stats: AdminStatsDTO) -> str:
    """
    Форматирование статистики для администратора

    Args:
        stats: DTO со статистикой

    Returns:
        Отформатированная статистика
    """
    lines = [
        f"Всего пользователей: {stats.total_users}",
        f"Участников: {stats.participants}",
        f"Организаторов: {stats.organizers}",
        f"Подписаны на напоминания: {stats.subscribed_users}",
    ]
    return "\n".join(lines)


def format_broadcast_result(sent: int, failed: int, total: int) -> str:
    """
    Форматирование результата рассылки

    Args:
        sent: успешно отправлено
        failed: не удалось отправить
        total: всего получателей

    Returns:
        Отформатированный результат
    """
    success_rate = (sent / total * 100) if total > 0 else 0

    result = "📨 *Результат рассылки:*\n\n"
    result += f"✅ Успешно: {sent}\n"
    result += f"❌ Ошибки: {failed}\n"
    result += f"📊 Всего: {total}\n"
    result += f"📈 Успешность: {success_rate:.1f}%\n"

    return result


def format_notification_status(enabled: bool) -> str:
    """
    Форматирование статуса уведомлений

    Args:
        enabled: включены ли уведомления

    Returns:
        Сообщение о статусе
    """
    if enabled:
        return "✅ Уведомления включены! Вы будете получать напоминания о важных событиях."
    else:
        return "🔕 Уведомления выключены. Вы не будете получать напоминания."


def format_welcome_message(username: str | None = None) -> str:
    """
    Форматирование приветственного сообщения

    Args:
        username: имя пользователя (опционально)

    Returns:
        Приветственное сообщение
    """
    name = username or "друг"
    return (
        f"👋 Привет, {name}!\n\n"
        f"Я — бот для участников хакатона. Я помогу:\n"
        f"• 📅 Узнать расписание событий\n"
        f"• 📋 Ознакомиться с правилами\n"
        f"• ❓ Получить ответы на частые вопросы\n"
        f"• 🔔 Включить напоминания\n\n"
        f"Используй команды из меню или введи /help для списка команд."
    )


def format_help_message(commands: list[dict]) -> str:
    # Обновленный список команд
    commands = [
        {"command": "/start", "description": "Начать работу с ботом"},
        {"command": "/help", "description": "Показать это сообщение"},
        {"command": "/select_hackathon", "description": "Посмотреть доступные хакатоны"},
        {
            "command": "/join КОД",
            "description": "Присоединиться к хакатону (например: /join HACK2024)",
        },
        {"command": "/hackathon", "description": "Информация о текущем хакатоне"},
        {"command": "/schedule", "description": "Расписание событий"},
        {"command": "/rules", "description": "Правила хакатона"},
        {"command": "/faq", "description": "Часто задаваемые вопросы"},
        {"command": "/notify_on", "description": "Включить уведомления"},
        {"command": "/notify_off", "description": "Выключить уведомления"},
        {"command": "/upcoming", "description": "Ближайшие события"},
        {"command": "/list_hackathons", "description": "Показать все хакатоны"},
        {"command": "/admin_stats", "description": "📊 Статистика (только для организаторов)"},
        {"command": "/admin_broadcast", "description": "📨 Рассылка (только для организаторов)"},
    ]

    result = "ℹ️ *Доступные команды:*\n\n"

    for cmd in commands:
        result += f"*{cmd['command']}* — {cmd['description']}\n"

    result += "\n📌 *Как начать:*\n"
    result += "1. Используйте /select_hackathon чтобы увидеть хакатоны\n"
    result += "2. Присоединитесь с помощью /join КОД_ХАКАТОНА\n"
    result += "3. Смотрите расписание, правила и FAQ\n\n"
    result += "Для использования просто введите команду."

    return result


def format_broadcast_preview(hackathon_name: str, user_count: int, message: str) -> str:
    """
    Форматирование предпросмотра рассылки

    Args:
        hackathon_name: название хакатона
        user_count: количество получателей
        message: текст сообщения для рассылки

    Returns:
        Отформатированный предпросмотр
    """
    preview = "📨 *Предпросмотр рассылки:*\n\n"
    preview += f"*Хакатон:* {hackathon_name}\n"
    preview += f"*Получателей:* {user_count}\n\n"
    preview += f"*Сообщение:*\n{message}\n\n"
    preview += "Подтвердите отправку:"

    return preview


def format_reminder_message(event, minutes_before: int) -> str:
    """Форматирование сообщения-напоминания с учетом интервала"""
    if minutes_before >= 60:
        hours = minutes_before // 60
        if hours == 1:
            time_text = "через 1 час"
        elif 2 <= hours <= 4:
            time_text = f"через {hours} часа"
        else:
            time_text = f"через {hours} часов"
    else:
        last_digit = minutes_before % 10
        if last_digit == 1 and minutes_before != 11:
            time_text = f"через {minutes_before} минуту"
        elif 2 <= last_digit <= 4 and not (12 <= minutes_before <= 14):
            time_text = f"через {minutes_before} минуты"
        else:
            time_text = f"Через *{minutes_before} минут*"

    message = f"🔔 *Напоминание*\n\n" f"{time_text}: *{event.title}*"

    if hasattr(event, "starts_at") and event.starts_at:
        time_str = event.starts_at.strftime("%H:%M")
        message += f"\n🕐 {time_str}"

    if hasattr(event, "location") and event.location:
        message += f"\n📍 {event.location}"

    return message
