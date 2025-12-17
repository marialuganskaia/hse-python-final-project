from dataclasses import dataclass

from .dto import (
    ReminderEventDTO,
    ReminderParticipantDTO,
    ReminderPileDTO,
)
from .ports import EventRepository, SubscriptionRepository


@dataclass
class ProcessRemindersUseCase:
    event_repo: EventRepository
    subscription_repo: SubscriptionRepository

    async def execute(self, hackathon_id: int, hours_ahead: int = 1) -> list[ReminderPileDTO]:
        events = await self.event_repo.get_upcoming_events(
            hackathon_id=hackathon_id, hours_ahead=hours_ahead
        )
        if not events:
            return []
        users = await self.subscription_repo.get_subscribed_users(hackathon_id)
        if not users:
            return []
        participants = [
            ReminderParticipantDTO(
                user_id=u.id,
                telegram_id=u.telegram_id,
            )
            for u in users
        ]
        result: list[ReminderPileDTO] = []
        for event in events:
            result.append(
                ReminderPileDTO(
                    event=ReminderEventDTO(
                        event_id=event.id, title=event.title, starts_at=event.starts_at
                    ),
                    participants=participants,
                )
            )
        return result
