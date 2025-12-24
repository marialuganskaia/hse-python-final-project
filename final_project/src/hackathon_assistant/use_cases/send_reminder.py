import logging
from dataclasses import dataclass

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from .dto import ReminderPileDTO
from .ports import Notifier

logger = logging.getLogger(__name__)


@dataclass
class SendRemindersUseCase:
    notifier: Notifier | None = None
    bot: Bot | None = None

    async def execute(self, piles: list[ReminderPileDTO]) -> None:
        if self.notifier is None and self.bot is None:
            raise RuntimeError("SendRemindersUseCase: set either notifier or bot")
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
                    if self.notifier is not None:
                        await self.notifier.send(telegram_id=p.telegram_id, text=text)
                    else:
                        await self.bot.send_message(  # type: ignore[union-attr]
                            chat_id=p.telegram_id,
                            text=text,
                            parse_mode="Markdown",
                        )

                    total_sent += 1
                    logger.info(
                        "Reminder sent to user %s (chat_id: %s)",
                        p.user_id,
                        p.telegram_id,
                    )

                except TelegramBadRequest as e:
                    if "chat not found" in str(e).lower():
                        logger.warning("Chat not found for user %s", p.user_id)
                    total_failed += 1

                except TelegramForbiddenError:
                    logger.warning("User %s blocked the bot", p.user_id)
                    total_failed += 1

                except Exception as e:  # noqa: BLE001
                    logger.error("Error sending reminder to user %s: %r", p.user_id, e)
                    total_failed += 1

            logger.info("Reminders sent: %s successful, %s failed", total_sent, total_failed)
