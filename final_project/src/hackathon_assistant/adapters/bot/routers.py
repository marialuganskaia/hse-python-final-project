from aiogram import Dispatcher

from .admin import admin_router
from .user import user_router


def setup_routers(dp: Dispatcher) -> None:
    dp.include_router(user_router)
    dp.include_router(admin_router)
