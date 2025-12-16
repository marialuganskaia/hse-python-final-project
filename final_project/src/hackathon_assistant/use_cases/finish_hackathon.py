from dataclasses import dataclass

from .ports import HackathonRepository, SubscriptionRepository


@dataclass
class FinishHackathonUseCase:
    hackathon_repo: HackathonRepository
    subscription_repo: SubscriptionRepository

    async def execute(self, hackathon_id: int) -> bool:
        hackathon = await self.hackathon_repo.get_by_id(hackathon_id)
        if hackathon is None:
            return False
        hackathon.is_active = False
        await self.hackathon_repo.save(hackathon)
        subscriptions = await self.subscription_repo.get_by_hackathon(hackathon_id)
        for subscription in subscriptions:
            subscription.enabled = False
            await self.subscription_repo.save(subscription)
        return True
