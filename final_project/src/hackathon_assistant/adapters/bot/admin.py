from aiogram import Router, types
from aiogram.filters import Command

admin_router = Router(name="admin_router")


@admin_router.message(Command("admin_stats"))
async def cmd_admin_stats(message: types.Message, use_cases) -> None:
    """Обработчик команды /admin_stats"""
    # TODO: проверить права администратора
    # TODO: вызвать use case, получить AdminStatsDTO
    # TODO: отформатировать статистику
    await message.answer("Статистика ещё не подключена.")


@admin_router.message(Command("admin_broadcast"))
async def cmd_admin_broadcast(message: types.Message, use_cases) -> None:
    """Обработчик команды /admin_broadcast"""
    # TODO: проверить права администратора
    # TODO: вызвать use case для рассылки
    # TODO: получить BroadcastTargetDTO список
    # TODO: показать результат рассылки
    await message.answer("Рассылка ещё не настроена.")
