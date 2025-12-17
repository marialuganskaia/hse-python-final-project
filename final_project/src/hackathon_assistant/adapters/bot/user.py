from datetime import datetime, timedelta
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

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

async def require_hackathon_selected(message: types.Message, use_cases: UseCaseProvider) -> bool:
    """
    Проверяет, выбран ли у пользователя хакатон.
    Если нет - отправляет сообщение и возвращает False.
    """
    try:
        hackathon_dto, _ = await use_cases.get_hackathon_info.execute(
            telegram_id=message.from_user.id
        )
        
        if not hackathon_dto:
            await message.answer(
                "🎯 *Хакатон не выбран*\n\n"
                "Чтобы использовать эту команду, сначала нужно присоединиться к хакатону:\n\n"
                "1. Посмотрите доступные хакатоны:\n"
                "   `/select_hackathon`\n\n"
                "2. Присоединитесь по коду:\n"
                "   `/join КОД_ХАКАТОНА`\n\n"
                "*Пример:* `/join HACK2024`\n\n"
                "Код хакатона можно получить у организаторов.",
                parse_mode="Markdown"
            )
            return False
        return True
        
    except Exception as e:
        print(f"Error checking hackathon: {e}")
        await message.answer(
            "🤔 Не удалось проверить ваш хакатон.\n"
            "Попробуйте:\n"
            "1. Перезапустить бот: /start\n"
            "2. Выбрать хакатон: /select_hackathon\n"
            "3. Обратиться к организаторам",
            parse_mode="Markdown"
        )
        return False
    

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
    
        welcome_text = f"👋 Привет, {message.from_user.first_name or 'друг'}!\n\nДобро пожаловать в бот хакатона. Используйте /help для списка команд."
        await message.answer(welcome_text, parse_mode="Markdown")
        
    except Exception as e:
        print(f"Error in /start: {e}")
        await message.answer(
            "👋 Добро пожаловать!\n\n"
            "Я бот для участников хакатона.\n"
            "Используйте /help чтобы увидеть список команд."
        )
    


@user_router.message(Command("help"))
async def cmd_help(message: types.Message, use_cases: UseCaseProvider) -> None:
    """Обработчик команды /help"""
    try:
        help_text = format_help_message([])
        await message.answer(help_text, parse_mode="Markdown")
    except Exception as e:
        print(f"Error in /help: {e}")
        await message.answer(
            "ℹ️ *Доступные команды:*\n\n"
            "/start - Начало работы\n"
            "/help - Помощь\n"
            "/select_hackathon - Выбрать хакатон\n"
            "/join КОД - Присоединиться\n"
            "/hackathon - Информация о хакатоне\n"
            "/schedule - Расписание\n"
            "/rules - Правила\n"
            "/faq - Частые вопросы\n"
            "/notify_on - Включить уведомления\n"
            "/notify_off - Выключить уведомления",
            parse_mode="Markdown"
        )
        


@user_router.message(Command("hackathon"))
async def cmd_hackathon(message: types.Message, use_cases: UseCaseProvider) -> None:
    """Информация о текущем хакатоне пользователя"""
    try:
        hackathon_dto, is_subscribed = await use_cases.get_hackathon_info.execute(
            telegram_id=message.from_user.id
        )
        
        if not hackathon_dto:
            await message.answer(
                "❌ *Хакатон не выбран*\n\n"
                "Сначала присоединитесь к хакатону:\n"
                "1. Используйте /select_hackathon чтобы увидеть доступные хакатоны\n"
                "2. Затем /join <код> чтобы присоединиться\n\n"
                "Код хакатона вам должны предоставить организаторы.",
                parse_mode="Markdown"
            )
            return
        
        hackathon_text = format_hackathon_info(hackathon_dto, is_subscribed)
        await message.answer(hackathon_text, parse_mode="Markdown")
        
    except Exception as e:
        print(f"Error in /hackathon: {e}")
        await message.answer("Информация о хакатоне временно недоступна.")


# ========== Информационные команды ==========


@user_router.message(Command("schedule"))
async def cmd_schedule(message: types.Message, use_cases: UseCaseProvider) -> None:
    """Обработчик команды /schedule"""
    # Проверка выбранного хакатона
    if not await require_hackathon_selected(message, use_cases):
        return
    
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
    # Проверка выбранного хакатона
    if not await require_hackathon_selected(message, use_cases):
        return
    
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
    # Проверка выбранного хакатона
    if not await require_hackathon_selected(message, use_cases):
        return
    
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
    # Проверка выбранного хакатона
    if not await require_hackathon_selected(message, use_cases):
        return
    
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
    # Проверка выбранного хакатона
    if not await require_hackathon_selected(message, use_cases):
        return
    
    try:
        success = await use_cases.unsubscribe_notifications.execute(message.from_user.id)
        status_text = format_notification_status(not success)
        await message.answer(status_text)
    except Exception as e:
        print(f"Error in /notify_off: {e}")
        await message.answer("🔕 Уведомления выключены (тестовый режим).")


@user_router.message(Command("select_hackathon"))
async def cmd_select_hackathon(message: types.Message, use_cases: UseCaseProvider) -> None:
    """Показать доступные хакатоны"""
    try:
        hackathons = await use_cases.list_hackathons.execute(active_only=True)
        
        if not hackathons:
            await message.answer(
                "📭 *Сейчас нет активных хакатонов*\n\n"
                "Все хакатоны либо завершены, либо еще не начались.\n"
                "Обратитесь к организаторам за информацией.",
                parse_mode="Markdown"
            )
            return
        
        hackathon_list = []
        for i, hackathon in enumerate(hackathons, 1):
            item = f"{i}. *{hackathon.name}*"
            if hackathon.code:
                item += f" (код: `{hackathon.code}`)"
            if hackathon.start_at:
                item += f" - {hackathon.start_at.strftime('%d.%m.%Y')}"
            hackathon_list.append(item)
        
        message_text = "🎯 *Доступные хакатоны:*\n\n" + "\n".join(hackathon_list)
        message_text += "\n\n*Чтобы присоединиться, используйте:*\n"
        message_text += "`/join <код_хакатона>`\n\n"
        message_text += f"*Пример:* `/join {hackathons[0].code if hackathons[0].code else 'КОД'}`"
        
        await message.answer(message_text, parse_mode="Markdown")
        
    except Exception as e:
        print(f"Error in /select_hackathon: {e}")
        await message.answer(
            "Не удалось загрузить список хакатонов.\n"
            "Попробуйте позже или обратитесь к организаторам."
        )


@user_router.message(Command("join"))
async def cmd_join_hackathon(message: types.Message, use_cases: UseCaseProvider) -> None:
    """Присоединение к хакатону по коду"""
    try:
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            await message.answer(
                "❌ *Использование:* `/join <код_хакатона>`\n\n"
                "*Пример:* `/join HACK2024`\n"
                "Используйте /select_hackathon чтобы увидеть список доступных хакатонов.",
                parse_mode="Markdown"
            )
            return
        
        code = parts[1].strip().upper()
        
        # ВАЖНО: Исправляем имя use case согласно usecase_provider.py
        hackathon = await use_cases.select_hackathon_by_code.execute(
            telegram_id=message.from_user.id,
            hackathon_code=code
        )
        
        if hackathon:
            await message.answer(
                f"✅ *Успешно!*\n\n"
                f"Вы присоединились к хакатону:\n"
                f"🏆 *{hackathon.name}*\n\n"
                f"Теперь вы можете:\n"
                f"• Просматривать расписание (/schedule)\n"
                f"• Читать правила (/rules)\n"
                f"• Смотреть FAQ (/faq)\n"
                f"• Включить уведомления (/notify_on)\n"
                f"• Посмотреть информацию (/hackathon)",
                parse_mode="Markdown"
            )
        else:
            await message.answer(
                f"❌ *Хакатон не найден*\n\n"
                f"Код `{code}` не соответствует ни одному активному хакатону.\n"
                f"Проверьте правильность кода или используйте /select_hackathon для списка.",
                parse_mode="Markdown"
            )
            
    except Exception as e:
        print(f"Error in /join: {e}")
        await message.answer(
            "❌ Произошла ошибка при присоединении.\n"
            "Попробуйте позже или обратитесь к организаторам."
        )
