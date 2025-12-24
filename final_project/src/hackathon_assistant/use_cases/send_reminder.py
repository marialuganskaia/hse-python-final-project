from __future__ import annotations

from dataclasses import dataclass
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from .dto import ReminderEventDTO, ReminderParticipantDTO, ReminderPileDTO

import logging

logger = logging.getLogger(__name__)

@dataclass
class SendRemindersUseCase:
    bot: Bot | None = None

    async def execute(self, piles: list[ReminderPileDTO]) -> None:
        total_sent = 0
        total_failed = 0
        
        for pile in piles:
            time_str = pile.event.starts_at.strftime("%H:%M")
            
            text = (
                f"🔔 *Напоминание*\n\n"
                f"Скоро событие:\n"
                f"📌 *{pile.event.title}*\n"
                f"🕐 {time_str}"
            )
            
            for p in pile.participants:
                try:
                    await self.bot.send_message(
                        chat_id=p.telegram_id,
                        text=text,
                        parse_mode="Markdown"
                    )
                    total_sent += 1
                    logger.info(f"Reminder sent to user {p.user_id} (chat_id: {p.telegram_id})")
                    
                except TelegramBadRequest as e:
                    if "chat not found" in str(e).lower():
                        logger.warning(f"Chat not found for user {p.user_id}")
                    total_failed += 1
                except TelegramForbiddenError:
                    logger.warning(f"User {p.user_id} blocked the bot")
                    total_failed += 1
                except Exception as e:
                    logger.error(f"Error sending reminder to user {p.user_id}: {e}")
                    total_failed += 1
        
        logger.info(f"Reminders sent: {total_sent} successful, {total_failed} failed")
