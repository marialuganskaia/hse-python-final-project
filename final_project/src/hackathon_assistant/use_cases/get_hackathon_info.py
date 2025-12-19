from dataclasses import dataclass

from .dto import HackathonDTO
from .ports import HackathonRepository, SubscriptionRepository, UserRepository


@dataclass
class GetHackathonInfoUseCase:
    user_repo: UserRepository
    hackathon_repo: HackathonRepository
    subscription_repo: SubscriptionRepository

    async def execute(self, telegram_id: int) -> tuple[HackathonDTO | None, bool]:
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user or not user.current_hackathon_id:
            return None, False

        hackathon = await self.hackathon_repo.get_by_id(user.current_hackathon_id)
        if not hackathon:
            return None, False

        subscription = await self.subscription_repo.get_user_subscription(
            user_id=user.id, hackathon_id=hackathon.id
        )
        is_subscribed = subscription is not None and subscription.enabled

        hackathon_dto = HackathonDTO(
            id=hackathon.id,
            name=hackathon.name,
            code=hackathon.code,
            description=hackathon.description,
            start_at=hackathon.start_at,
            end_at=hackathon.end_at,
            is_active=hackathon.is_active,
            location=hackathon.location if hasattr(hackathon, 'location') else None
        )

        return hackathon_dto, is_subscribed
