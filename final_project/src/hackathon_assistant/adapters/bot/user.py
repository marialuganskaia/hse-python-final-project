from aiogram import Router, types
from aiogram.filters import Command

user_router = Router(name="user_router")

# ========== Основные команды ==========

@user_router.message(Command("start"))
async def cmd_start(message: types.Message, use_cases) -> None:
    """Обработчик команды /start"""
    # TODO: вызвать use case для регистрации пользователя
    # TODO: получить StartResponse
    # TODO: отформатировать приветственное сообщение
    await message.answer("Добро пожаловать! Бот ещё не настроен.")


@user_router.message(Command("help"))
async def cmd_help(message: types.Message, use_cases) -> None:
    """Обработчик команды /help"""
    # TODO: вызвать use case для получения списка команд
    # TODO: отформатировать справку
    await message.answer("Справка ещё не готова.")


@user_router.message(Command("hackathon"))
async def cmd_hackathon(message: types.Message, use_cases) -> None:
    """Обработчик команды /hackathon"""
    # TODO: вызвать use case для получения информации о хакатоне
    # TODO: получить HackathonDTO
    # TODO: отформатировать информацию
    await message.answer("Информация о хакатоне ещё не подключена.")


# ========== Информационные команды ==========

@user_router.message(Command("schedule"))
async def cmd_schedule(message: types.Message, use_cases) -> None:
    """Обработчик команды /schedule"""
    # TODO: вызвать use case, получить ScheduleItemDTO список
    # TODO: отформатировать расписание
    await message.answer("Расписание ещё не подключено.")


@user_router.message(Command("rules"))
async def cmd_rules(message: types.Message, use_cases) -> None:
    """Обработчик команды /rules"""
    # TODO: вызвать use case, получить RulesDTO
    # TODO: отправить правила
    await message.answer("Правила ещё не загружены.")


@user_router.message(Command("faq"))
async def cmd_faq(message: types.Message, use_cases) -> None:
    """Обработчик команды /faq"""
    # TODO: вызвать use case, получить FAQItemDTO список
    # TODO: отформатировать FAQ
    await message.answer("FAQ ещё не подготовлен.")


# ========== Уведомления ==========

@user_router.message(Command("notify_on"))
async def cmd_notify_on(message: types.Message, use_cases) -> None:
    """Обработчик команды /notify_on"""
    # TODO: вызвать use case для включения уведомлений
    # TODO: показать статус подписки
    await message.answer("Уведомления ещё не настроены.")


@user_router.message(Command("notify_off"))
async def cmd_notify_off(message: types.Message, use_cases) -> None:
    """Обработчик команды /notify_off"""
    # TODO: вызвать use case для выключения уведомлений
    # TODO: показать статус подписки
    await message.answer("Уведомления ещё не настроены.")
