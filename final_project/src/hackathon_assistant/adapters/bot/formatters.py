"""Форматирование ответов бота"""

from datetime import datetime
from typing import List, Optional

from hackathon_assistant.use_cases.dto import (
    ScheduleItemDTO, 
    FAQItemDTO, 
    RulesDTO,
    HackathonDTO,
    AdminStatsDTO
)


def format_schedule(items: List[ScheduleItemDTO]) -> str:
    """
    Форматирование расписания в текст для Telegram
    
    Args:
        items: список элементов расписания
        
    Returns:
        Отформатированная строка с расписанием
    """
    if not items:
        return "📅 Расписание пока пустое.\n"
    
    # Группируем по дням
    items_by_day = {}
    for item in items:
        day_key = item.starts_at.strftime("%d.%m.%Y")
        if day_key not in items_by_day:
            items_by_day[day_key] = []
        items_by_day[day_key].append(item)
    
    # Форматируем
    result = "📅 *Расписание:*\n\n"
    
    for day, day_items in sorted(items_by_day.items()):
        result += f"*📆 {day}:*\n"
        
        # Сортируем события по времени начала
        day_items.sort(key=lambda x: x.starts_at)
        
        for item in day_items:
            # Форматируем время
            time_str = f"{item.starts_at.strftime('%H:%M')}–{item.ends_at.strftime('%H:%M')}"
            
            result += f"  • *{item.title}* ({time_str})\n"
            
            if item.location:
                result += f"    📍 {item.location}\n"
            if item.description:
                # Обрезаем длинное описание
                desc = item.description[:100] + "..." if len(item.description) > 100 else item.description
                result += f"    📝 {desc}\n"
            
            result += "\n"
    
    return result


def format_faq(items: List[FAQItemDTO]) -> str:
    """
    Форматирование FAQ в текст для Telegram
    
    Args:
        items: список вопросов-ответов
        
    Returns:
        Отформатированная строка с FAQ
    """
    if not items:
        return "❓ Часто задаваемые вопросы пока не добавлены.\n"
    
    result = "❓ *Часто задаваемые вопросы:*\n\n"
    
    for i, item in enumerate(items, 1):
        result += f"*{i}. {item.question}*\n"
        result += f"{item.answer}\n\n"
    
    return result


def format_rules(rules: Optional[RulesDTO]) -> str:
    """
    Форматирование правил в текст для Telegram
    
    Args:
        rules: DTO с правилами или None
        
    Returns:
        Отформатированные правила или сообщение об их отсутствии
    """
    if not rules or not rules.content:
        return "📋 Правила для этого хакатона пока не установлены.\n"
    
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
    
    result = f"📨 *Результат рассылки:*\n\n"
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


def format_welcome_message(username: Optional[str] = None) -> str:
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


def format_help_message(commands: List[dict]) -> str:
    """
    Форматирование справки по командам
    
    Args:
        commands: список команд с описанием
        
    Returns:
        Отформатированная справка
    """
    if not commands:
        # Заглушка, если команды еще не передаются
        commands = [
            {"command": "/start", "description": "Начало работы"},
            {"command": "/help", "description": "Помощь по командам"},
            {"command": "/hackathon", "description": "Информация о хакатоне"},
            {"command": "/schedule", "description": "Расписание событий"},
            {"command": "/rules", "description": "Правила хакатона"},
            {"command": "/faq", "description": "Часто задаваемые вопросы"},
            {"command": "/notify_on", "description": "Включить уведомления"},
            {"command": "/notify_off", "description": "Выключить уведомления"},
        ]
    
    result = "ℹ️ *Доступные команды:*\n\n"
    
    for cmd in commands:
        result += f"*{cmd['command']}* — {cmd['description']}\n"
    
    result += "\nДля использования просто введите команду или выберите из меню."
    
    return result
