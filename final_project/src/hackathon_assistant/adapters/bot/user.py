from datetime import datetime, timedelta

from aiogram import Router, types
from aiogram.filters import Command

from hackathon_assistant.infra.usecase_provider import UseCaseProvider
from hackathon_assistant.use_cases.dto import ScheduleItemDTO

from .formatters import (
    format_faq,
    format_hackathon_info,
    format_help_message,
    format_notification_status,
    format_rules,
    format_schedule,
    format_welcome_message,
)

user_router = Router(name="user_router")


# ========== Основные команды ==========


@user_router.message(Command("start"))
async def cmd_start(message: types.Message, use_cases: UseCaseProvider) -> None:
    """Обработчик команды /start"""
    try:
        __user = await use_cases.start_user.execute(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
        welcome_text = format_welcome_message(message.from_user.first_name)
        await message.answer(welcome_text, parse_mode="Markdown")
    except Exception as e:
        print(f"Error in /start: {e}")
        await message.answer("Привет! Начинаем работу.")


@user_router.message(Command("help"))
async def cmd_help(message: types.Message, use_cases: UseCaseProvider) -> None:
    """Обработчик команды /help"""
    help_text = format_help_message([])
    await message.answer(help_text, parse_mode="Markdown")


@user_router.message(Command("hackathon"))
async def cmd_hackathon(message: types.Message, use_cases: UseCaseProvider) -> None:
    """Обработчик команды /hackathon"""
    try:
        hackathons = await use_cases.list_hackathons.execute(active_only=True)

        if not hackathons:
            await message.answer("Сейчас нет активных хакатонов.")
            return

        first_hackathon = hackathons[0]
        is_subscribed = False

        hackathon_text = format_hackathon_info(first_hackathon, is_subscribed)
        await message.answer(hackathon_text, parse_mode="Markdown")
    except Exception as e:
        print(f"Error in /hackathon: {e}")
        await message.answer("Информация о хакатоне временно недоступна.")


# ========== Информационные команды ==========


@user_router.message(Command("schedule"))
async def cmd_schedule(message: types.Message, use_cases: UseCaseProvider) -> None:
    """Обработчик команды /schedule"""
    try:
        schedule_items = await use_cases.get_schedule.execute(message.from_user.id)

        if not schedule_items:
            # Тестовые данные если расписание пустое
            test_items = [
                ScheduleItemDTO(
                    title="Регистрация участников",
                    starts_at=datetime.now() + timedelta(hours=1),
                    ends_at=datetime.now() + timedelta(hours=2),
                    location="Главный холл",
                    description="Регистрация и выдача бейджей",
                ),
                ScheduleItemDTO(
                    title="Открытие хакатона",
                    starts_at=datetime.now() + timedelta(hours=3),
                    ends_at=datetime.now() + timedelta(hours=4),
                    location="Аудитория 101",
                    description="Приветственная речь организаторов",
                ),
            ]
            schedule_text = format_schedule(test_items)
        else:
            schedule_text = format_schedule(schedule_items)

        await message.answer(schedule_text, parse_mode="Markdown")
    except Exception as e:
        print(f"Error in /schedule: {e}")
        # Тестовые данные при ошибке
        test_items = [
            ScheduleItemDTO(
                title="Тестовое событие",
                starts_at=datetime.now(),
                ends_at=datetime.now() + timedelta(hours=2),
                location="Тестовая локация",
                description="Это тестовое событие для демонстрации",
            ),
        ]
        schedule_text = format_schedule(test_items)
        await message.answer(schedule_text, parse_mode="Markdown")


@user_router.message(Command("rules"))
async def cmd_rules(message: types.Message, use_cases: UseCaseProvider) -> None:
    """Обработчик команды /rules"""
    try:
        rules_dto = await use_cases.get_rules.execute(message.from_user.id)
        rules_text = format_rules(rules_dto)
        await message.answer(rules_text, parse_mode="Markdown")
    except Exception as e:
        print(f"Error in /rules: {e}")
        await message.answer(
            "📋 *Правила хакатона:*\n\n1. Уважайте других участников\n2. Соблюдайте дедлайны\n3. Не используйте чужой код\n4. Веселитесь и учитесь!",
            parse_mode="Markdown",
        )


@user_router.message(Command("faq"))
async def cmd_faq(message: types.Message, use_cases: UseCaseProvider) -> None:
    """Обработчик команды /faq"""
    try:
        faq_items = await use_cases.get_faq.execute(message.from_user.id)
        faq_text = format_faq(faq_items)
        await message.answer(faq_text, parse_mode="Markdown")
    except Exception as e:
        print(f"Error in /faq: {e}")
        await message.answer(
            "❓ *Часто задаваемые вопросы:*\n\n*1. Какой размер команды?*\nОт 2 до 5 человек.\n\n*2. Можно ли участвовать онлайн?*\nДа, есть онлайн-трек.\n\n*3. Где взять код хакатона?*\nУ организаторов или в группе.",
            parse_mode="Markdown",
        )


# ========== Уведомления ==========


@user_router.message(Command("notify_on"))
async def cmd_notify_on(message: types.Message, use_cases: UseCaseProvider) -> None:
    """Обработчик команды /notify_on"""
    try:
        success = await use_cases.subscribe_notifications.execute(message.from_user.id)
        status_text = format_notification_status(success)
        await message.answer(status_text)
    except Exception as e:
        print(f"Error in /notify_on: {e}")
        await message.answer("✅ Уведомления включены (тестовый режим).")


@user_router.message(Command("notify_off"))
async def cmd_notify_off(message: types.Message, use_cases: UseCaseProvider) -> None:
    """Обработчик команды /notify_off"""
    try:
        success = await use_cases.unsubscribe_notifications.execute(message.from_user.id)
        status_text = format_notification_status(not success)
        await message.answer(status_text)
    except Exception as e:
        print(f"Error in /notify_off: {e}")
        await message.answer("🔕 Уведомления выключены (тестовый режим).")
