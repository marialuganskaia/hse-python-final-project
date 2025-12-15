from aiogram import Router, types
from aiogram.filters import Command

from hackathon_assistant.infra.usecase_provider import UseCaseProvider

user_router = Router(name="user_router")


# ========== Основные команды ==========


@user_router.message(Command("start"))
async def cmd_start(message: types.Message, use_cases: UseCaseProvider) -> None:
    """Обработчик команды /start"""
    await use_cases.start_user.execute(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )
    # TODO: сформировать приветственный текст, предложить выбрать хакатон
    await message.answer(
        f"Привет, {message.from_user.first_name}! Ты зарегистрирован в системе бота."
    )


@user_router.message(Command("help"))
async def cmd_help(message: types.Message, use_cases: UseCaseProvider) -> None:
    """Обработчик команды /help"""
    # TODO: вызвать use case для получения списка команд
    # TODO: отформатировать справку
    help_text = """
    Доступные команды:
    /start - Начало работы
    /help - Помощь
    /hackathon - Информация о хакатоне
    /schedule - Расписание
    /rules - Правила
    /faq - Частые вопросы
    /notify_on - Включить уведомления
    /notify_off - Выключить уведомления
    """
    await message.answer(help_text)


@user_router.message(Command("hackathon"))
async def cmd_hackathon(message: types.Message, use_cases: UseCaseProvider) -> None:
    """Обработчик команды /hackathon"""
    # TODO: вызвать use case для получения информации о хакатоне
    # Получим список активных хакатонов
    hackathons = await use_cases.list_hackathons.execute(active_only=True)

    if not hackathons:
        await message.answer("Сейчас нет активных хакатонов.")
        return

    # TODO: получить информацию о текущем хакатоне пользователя
    await message.answer("Информация о хакатоне ещё не подключена.")


# ========== Информационные команды ==========


@user_router.message(Command("schedule"))
async def cmd_schedule(message: types.Message, use_cases: UseCaseProvider) -> None:
    """Обработчик команды /schedule"""
    schedule_items = await use_cases.get_schedule.execute(message.from_user.id)

    if not schedule_items:
        await message.answer("Расписание пока пустое или не настроено.")
        return

    # Форматируем расписание
    schedule_text = "📅 Расписание:\n\n"
    for item in schedule_items:
        schedule_text += f"• {item.title}\n"
        schedule_text += (
            f"  🕐 {item.starts_at.strftime('%H:%M')} - {item.ends_at.strftime('%H:%M')}\n"
        )
        if item.location:
            schedule_text += f"  📍 {item.location}\n"
        if item.description:
            schedule_text += f"  📝 {item.description}\n"
        schedule_text += "\n"

    await message.answer(schedule_text)


@user_router.message(Command("rules"))
async def cmd_rules(message: types.Message, use_cases: UseCaseProvider) -> None:
    """Обработчик команды /rules"""
    rules_dto = await use_cases.get_rules.execute(message.from_user.id)

    if not rules_dto:
        await message.answer("Правила для текущего хакатона не найдены.")
        return

    rules_text = f"📋 Правила хакатона:\n\n{rules_dto.content}"
    await message.answer(rules_text)


@user_router.message(Command("faq"))
async def cmd_faq(message: types.Message, use_cases: UseCaseProvider) -> None:
    """Обработчик команды /faq"""
    faq_items = await use_cases.get_faq.execute(message.from_user.id)

    if not faq_items:
        await message.answer("FAQ для текущего хакатона пока пустой.")
        return

    # Форматируем FAQ
    faq_text = "❓ Часто задаваемые вопросы:\n\n"
    for i, item in enumerate(faq_items, 1):
        faq_text += f"{i}. {item.question}\n"
        faq_text += f"   Ответ: {item.answer}\n\n"

    await message.answer(faq_text)


# ========== Уведомления ==========


@user_router.message(Command("notify_on"))
async def cmd_notify_on(message: types.Message, use_cases: UseCaseProvider) -> None:
    """Обработчик команды /notify_on"""
    success = await use_cases.subscribe_notifications.execute(message.from_user.id)

    if success:
        await message.answer("✅ Уведомления включены! Буду напоминать о важных событиях.")
    else:
        await message.answer(
            "❌ Не удалось включить уведомления. Сначала выберите хакатон (/hackathon)."
        )


@user_router.message(Command("notify_off"))
async def cmd_notify_off(message: types.Message, use_cases: UseCaseProvider) -> None:
    """Обработчик команды /notify_off"""
    success = await use_cases.unsubscribe_notifications.execute(message.from_user.id)

    if success:
        await message.answer("🔕 Уведомления выключены. Вы больше не будете получать напоминания.")
    else:
        await message.answer(
            "⚠️ Не удалось выключить уведомления. Возможно, они уже были выключены."
        )
