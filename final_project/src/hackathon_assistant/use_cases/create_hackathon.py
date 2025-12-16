from dataclasses import dataclass
from typing import Any

from ..domain.models import Hackathon, Event, FAQItem, Rules
from .ports import HackathonRepository, EventRepository, FAQRepository, RulesRepository


@dataclass
class CreateHackathonFromConfigUseCase:
    hackathon_repo: HackathonRepository
    event_repo: EventRepository
    faq_repo: FAQRepository
    rules_repo: RulesRepository

    async def execute(self, config: dict[str, Any]) -> Hackathon:
        """
        Создать хакатон из конфига

        config = {
            "name": str,
            "code": str,
            "description": str | None,
            "start_at": datetime,
            "end_at": datetime,
            "is_active": bool,
            "events": [ {title, type, starts_at, ends_at, description, location}],
            "rules": {content: str},
            "faq": [ {question, answer}]
        }
        """

        hackathon = Hackathon(
            id=None,
            name=config["name"],
            code=config["code"],
            description=config.get("description"),
            start_at=config["start_at"],
            end_at=config["end_at"],
            is_active=config.get("is_active", True),
        )
        saved_hackathon = await self.hackathon_repo.save(hackathon)

        hackathon_id = saved_hackathon.id

        events = [
            Event(
                id=None,
                hackathon_id=hackathon_id,
                title=e["title"],
                type=e["type"],
                starts_at=e["starts_at"],
                ends_at=e["ends_at"],
                location=e.get("location"),
                description=e.get("description"),
            )
            for e in config.get("events", [])
        ]
        if events:
            await self.event_repo.save_all(events)

        rules_data = config.get("rules")
        if rules_data:
            rules = Rules(hackathon_id=hackathon_id, content=rules_data["content"])
            await self.rules_repo.save(rules)

        faq_items = [
            FAQItem(
                hackathon_id=hackathon_id,
                question=f["question"],
                answer=f["answer"],
            )
            for f in config.get("faq", [])
        ]
        if faq_items:
            await self.faq_repo.save_all(faq_items)

        return saved_hackathon
