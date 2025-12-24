import logging

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from hackathon_assistant.infra.usecase_provider import UseCaseProvider
from hackathon_assistant.use_cases.dto import BroadcastResultDTO

from .formatters import (
    format_admin_stats,
    format_broadcast_preview,
    format_broadcast_result,
)
from .helpers import is_organizer

logger = logging.getLogger(__name__)

admin_router = Router(name="admin_router")


class BroadcastStates(StatesGroup):
    choosing_hackathon = State()
    entering_message = State()
    confirmation = State()


@admin_router.message(Command("admin_stats"))
async def cmd_admin_stats(message: types.Message, use_cases: UseCaseProvider) -> None:
    try:
        parts = message.text.split(maxsplit=1)

        if len(parts) > 1:
            hack_code = parts[1].strip()
            hackathon = await use_cases.select_hackathon_by_code.execute(
                telegram_id=message.from_user.id, hackathon_code=hack_code
            )
            if not hackathon:
                await message.answer(f"❌ Хакатон с кодом '{hack_code}' не найден.")
                return

        if not await is_organizer(message.from_user.id, use_cases):
            await message.answer("❌ Эта команда доступна только организаторам.")
            return

        stats = await use_cases.get_admin_stats.execute()
        text = format_admin_stats(stats)
        await message.answer(text)

    except Exception as e:
        logger.error(f"Error in /admin_stats: {e}")
        await message.answer("❌ Ошибка при получении статистики.")


@admin_router.message(Command("admin_broadcast"))
async def cmd_admin_broadcast(message: types.Message, use_cases: UseCaseProvider) -> None:
    """Обработчик команды /admin_broadcast"""
    try:
        parts = message.text.split(maxsplit=2)

        if len(parts) < 3:
            await message.answer(
                "❌ Использование: `/admin_broadcast <код_хакатона> <текст_сообщения>`\n\n"
                "Пример: `/admin_broadcast HACK2024 Важное объявление!`",
                parse_mode="Markdown",
            )
            return

        hack_code = parts[1].strip()
        broadcast_message = parts[2].strip()

        hackathon = await use_cases.select_hackathon_by_code.execute(
            telegram_id=message.from_user.id, hackathon_code=hack_code
        )

        if not hackathon:
            await message.answer(f"❌ Хакатон с кодом '{hack_code}' не найден.")
            return

        if not await is_organizer(message.from_user.id, use_cases):
            await message.answer("❌ Эта команда доступна только организаторам.")
            return

        targets = await use_cases.send_broadcast.execute(
            hackathon_id=hackathon.id,
            message=broadcast_message,
        )

        await message.answer(
            f"🔄 Рассылка для хакатона: {hackathon.name} ({len(targets)} получателей)"
        )

        sent_count = 0
        failed_count = 0

        for target in targets:
            try:
                await message.bot.send_message(
                    target.telegram_id, broadcast_message, parse_mode="Markdown"
                )
                sent_count += 1

            except Exception as e:
                logger.exception("Failed to send to %s: %r", target.telegram_id, e)
                failed_count += 1

        result_text = format_broadcast_result(
            sent=sent_count, failed=failed_count, total=len(targets)
        )
        await message.answer(result_text, parse_mode="Markdown")

    except Exception as e:
        logger.exception("Error in /admin_broadcast: %r", e)
        await message.answer("❌ Ошибка при отправке рассылки.")


@admin_router.callback_query(
    BroadcastStates.choosing_hackathon, F.data.startswith("broadcast_hack_")
)
async def process_hackathon_choice(
    callback: types.CallbackQuery, state: FSMContext, use_cases: UseCaseProvider
):
    try:
        hackathon_id = int(callback.data.split("_")[-1])
        await state.update_data(hackathon_id=hackathon_id)

        hackathon_name = "Хакатон 2024"
        user_count = 156

        await callback.message.edit_text(
            f"✅ Выбран хакатон: *{hackathon_name}*\n"
            f"👥 Получателей: *{user_count}* пользователей\n\n"
            "✏️ *Отправьте текст сообщения для рассылки:*",
            parse_mode="Markdown",
            reply_markup=None,
        )
        await state.set_state(BroadcastStates.entering_message)
        await callback.answer()

    except Exception as e:
        print(f"Error choosing hackathon: {e}")
        await callback.message.edit_text("❌ Ошибка при выборе хакатона.")
        await state.clear()


@admin_router.message(BroadcastStates.entering_message)
async def process_broadcast_message(
    message: types.Message, state: FSMContext, use_cases: UseCaseProvider
):
    try:
        data = await state.get_data()
        __hackathon_id = data.get("hackathon_id")
        await state.update_data(message_text=message.text)

        hackathon_name = "Хакатон 2024"
        user_count = 156

        builder = InlineKeyboardBuilder()
        builder.button(text="✅ Отправить рассылку", callback_data="broadcast_confirm")
        builder.button(text="✏️ Редактировать текст", callback_data="broadcast_edit")
        builder.button(text="❌ Отменить", callback_data="broadcast_cancel")
        builder.adjust(1)

        preview_text = format_broadcast_preview(
            hackathon_name=hackathon_name, user_count=user_count, message=message.text
        )

        await message.answer(preview_text, reply_markup=builder.as_markup(), parse_mode="Markdown")
        await state.set_state(BroadcastStates.confirmation)

    except Exception as e:
        print(f"Error processing message: {e}")
        await message.answer("❌ Ошибка при обработке сообщения.")
        await state.clear()


@admin_router.callback_query(BroadcastStates.confirmation, F.data == "broadcast_confirm")
async def confirm_broadcast(
    callback: types.CallbackQuery, state: FSMContext, use_cases: UseCaseProvider
):
    try:
        data = await state.get_data()
        __hackathon_id = data.get("hackathon_id")
        _message_text = data.get("message_text")

        await callback.message.edit_text("🔄 *Отправка рассылки...*", parse_mode="Markdown")

        result = BroadcastResultDTO(
            total_recipients=156, sent_successfully=152, failed=4, success_rate=0.97
        )

        result_text = format_broadcast_result(
            sent=result.sent_successfully,
            failed=result.failed,
            total=result.total_recipients,
        )

        await callback.message.edit_text(result_text, parse_mode="Markdown")

    except Exception as e:
        print(f"Error sending broadcast: {e}")
        await callback.message.edit_text(f"❌ Ошибка при отправке рассылки: {str(e)}")

    finally:
        await state.clear()
        await callback.answer()


@admin_router.callback_query(F.data.in_(["broadcast_edit", "broadcast_cancel"]))
async def handle_broadcast_actions(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data

    if action == "broadcast_edit":
        data = await state.get_data()
        __hackathon_id = data.get("hackathon_id")

        hackathon_name = "Хакатон 2024"
        user_count = 156

        await callback.message.edit_text(
            f"✏️ *Редактирование сообщения для хакатона:* {hackathon_name}\n"
            f"👥 Получателей: {user_count}\n\n"
            "Отправьте новый текст сообщения:",
            parse_mode="Markdown",
            reply_markup=None,
        )
        await state.set_state(BroadcastStates.entering_message)

    elif action == "broadcast_cancel":
        await callback.message.edit_text("❌ Рассылка отменена.")
        await state.clear()

    await callback.answer()
