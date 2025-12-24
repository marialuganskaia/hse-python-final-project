import asyncio
import logging
from aiogram import Bot
from hackathon_assistant.use_cases.dto import (
    ReminderEventDTO, 
    ReminderParticipantDTO, 
    ReminderPileDTO
)

logger = logging.getLogger(__name__)

class ReminderService:
    def __init__(self, bot: Bot, use_case_provider_factory):
        self.bot = bot
        self.use_case_provider_factory = use_case_provider_factory
        self._task: asyncio.Task | None = None
        logger.info("ReminderService initialized")

    async def start_periodic_reminders(self, interval_minutes: int = 5):
        if self._task and not self._task.done():
            logger.warning("Reminder task already running")
            return

        self._task = asyncio.create_task(self._periodic_reminder_task(interval_minutes))
        logger.info(f"Periodic reminders started (interval: {interval_minutes} min)")

    async def stop_periodic_reminders(self):
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            logger.info("Periodic reminders stopped")

    async def _periodic_reminder_task(self, interval_minutes: int):
        try:
            while True:
                await self.send_upcoming_event_reminders()
                await asyncio.sleep(interval_minutes * 60)
        except asyncio.CancelledError:
            logger.info("Reminder task cancelled")
        except Exception as e:
            logger.error(f"Reminder task error: {e}")

    async def send_upcoming_event_reminders(self):
        logger.info("Checking for upcoming events...")
        try:
            async with self.use_case_provider_factory() as use_cases:
                hackathons = await use_cases.list_hackathons.execute(active_only=True)
                
                for hackathon in hackathons:
                    events_2h = await use_cases.get_upcoming_events.execute(
                        hackathon_id=hackathon.id,
                        minutes_ahead=120
                    )
                    
                    events_15min = await use_cases.get_upcoming_events.execute(
                        hackathon_id=hackathon.id,
                        minutes_ahead=15
                    )
                    
                    if events_2h:
                        await self._send_reminders_for_events(
                            use_cases, hackathon.id, events_2h, 120
                        )
                    
                    if events_15min:
                        await self._send_reminders_for_events(
                            use_cases, hackathon.id, events_15min, 15
                        )
                        
        except Exception as e:
            logger.error(f"Error in send_upcoming_event_reminders: {e}")

    async def _send_reminders_for_events(self, use_cases, hackathon_id: int, events: list, interval_minutes: int):
        try:
            if not events:
                return
            
            participants = await self._get_hackathon_participants(use_cases, hackathon_id)
            
            if not participants:
                logger.warning(f"No participants found for hackathon {hackathon_id}")
                return
            
            reminder_piles = []
            
            for event in events:
                reminder_event = ReminderEventDTO(
                    event_id=event.id,
                    title=event.title,
                    starts_at=event.starts_at
                )
                
                participant_dtos = [
                    ReminderParticipantDTO(
                        user_id=user.id,
                        telegram_id=user.telegram_id
                    )
                    for user in participants
                ]
                
                pile = ReminderPileDTO(
                    event=reminder_event,
                    participants=participant_dtos
                )
                reminder_piles.append(pile)
            
            if reminder_piles:
                total_participants = sum(len(p.participants) for p in reminder_piles)
                logger.info(f"Sending reminders for {len(reminder_piles)} events to {total_participants} users")
                await use_cases.send_reminders.execute(reminder_piles)
                
        except Exception as e:
            logger.error(f"Error sending reminders for events: {e}")

    async def _get_hackathon_participants(self, use_cases, hackathon_id: int):
        try:
            hackathon_info = await use_cases.get_hackathon_info.execute(
                hackathon_id=hackathon_id,
                user_id=None
            )
            
            return []
            
        except Exception as e:
            logger.error(f"Error getting hackathon participants: {e}")
            return []
    