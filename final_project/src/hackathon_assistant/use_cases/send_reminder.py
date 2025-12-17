from dataclasses import dataclass
from .ports import Notifier
from .dto import ReminderPileDTO


@dataclass
class SendRemindersUseCase:
    notifier: Notifier

    async def execute(self, piles: list[ReminderPileDTO]) -> None:
        for pile in piles:
            text = (
                f"Скоро событие!\n\n"
                f"{pile.event.title}\n"
                f"Начало: {pile.event.starts_at}"
            )
            for p in pile.participants:
                await self.notifier.send(
                    telegram_id=p.telegram_id,
                    text=text,
                )
