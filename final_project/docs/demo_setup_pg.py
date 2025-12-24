import asyncio
import os
from datetime import datetime, timedelta

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from hackathon_assistant.adapters.db.models import (
    EventORM,
    FAQItemORM,
    HackathonORM,
    ReminderSubscriptionORM,
    RulesORM,
    UserORM,
)
from hackathon_assistant.adapters.db.repositories import (
    EventRepo,
    FAQRepo,
    HackathonRepo,
    RulesRepo,
    SubscriptionRepo,
    UserRepo,
)
from hackathon_assistant.domain.models import (
    Event,
    EventType,
    FAQItem,
    Hackathon,
    ReminderSubscription,
    Rules,
    User,
    UserRole,
)

DEMO_CODE = "DEMOHACK"


async def setup_demo() -> None:
    db_url = os.environ["DATABASE_URL"]  # в compose он уже есть
    engine = create_async_engine(db_url)

    Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with Session() as session:
        hackathon_id: int | None = None

        existing = (
            await session.execute(select(HackathonORM).where(HackathonORM.code == DEMO_CODE))
        ).scalars().first()
        if existing is not None:
            hackathon_id = existing.id

            await session.execute(
                delete(ReminderSubscriptionORM).where(ReminderSubscriptionORM.hackathon_id == hackathon_id))
            await session.execute(delete(EventORM).where(EventORM.hackathon_id == hackathon_id))
            await session.execute(delete(FAQItemORM).where(FAQItemORM.hackathon_id == hackathon_id))
            await session.execute(
                delete(RulesORM).where(RulesORM.hackathon_id == hackathon_id))
            await session.execute(delete(UserORM).where(UserORM.current_hackathon_id == hackathon_id))
            await session.execute(delete(HackathonORM).where(HackathonORM.id == hackathon_id))
            await session.commit()

        user_repo = UserRepo(session)
        hackathon_repo = HackathonRepo(session)
        event_repo = EventRepo(session)
        faq_repo = FAQRepo(session)
        rules_repo = RulesRepo(session)
        subscription_repo = SubscriptionRepo(session)

        now = datetime.now()

        hackathon = Hackathon(
            code=DEMO_CODE,
            name="Challenge 2025",
            description="Самый клевый хакатон по питону!",
            start_at=now - timedelta(days=2),
            end_at=now + timedelta(days=4),
            is_active=True,
            location="Вышка, Москва",
            id=None,
        )
        saved_hackathon = await hackathon_repo.save(hackathon)

        events = [
            Event(
                id=None,
                hackathon_id=saved_hackathon.id,
                title="Регистрация и кофе-брейк",
                type=EventType.MEETUP,
                starts_at=now - timedelta(hours=3),
                ends_at=now - timedelta(hours=1),
                location="1 этаж",
                description="Еда, кофе, знакомство",
            ),
            Event(
                id=None,
                hackathon_id=saved_hackathon.id,
                title="Чекпоинт 1: Идея",
                type=EventType.CHECKPOINT,
                starts_at=now + timedelta(minutes=20),
                ends_at=now + timedelta(hours=1),
                location="Атриум",
                description="Представьте идеи",
            ),
            Event(
                id=None,
                hackathon_id=saved_hackathon.id,
                title="Лекция: как с помощью питона зарабатывать много денег",
                type=EventType.LECTURE,
                starts_at=now + timedelta(hours=3),
                ends_at=now + timedelta(hours=4),
                location="R308",
                description="Разбираем реальные кейсы",
            ),
            Event(
                id=None,
                hackathon_id=saved_hackathon.id,
                title="Сдача проектов",
                type=EventType.DEADLINE,
                starts_at=now + timedelta(days=1, hours=10),
                ends_at=now + timedelta(days=1, hours=12),
                location="Онлайн-форма",
                description="Дедлайн подачи проектов",
            ),
        ]
        await event_repo.save_all(events)

        faq_items = [
            FAQItem(
                hackathon_id=saved_hackathon.id,
                question="Как подать проект?",
                answer="Проекты подаются через онлайн-форму. Ссылка появится за час до дедлайна",
            ),
            FAQItem(
                hackathon_id=saved_hackathon.id,
                question="Где взять доступ к данным?",
                answer="Все датасеты доступны по ссылке в описании хакатона. Нужен VPN для доступа.",
            ),
            FAQItem(
                hackathon_id=saved_hackathon.id,
                question="Можно ли участвовать одному?",
                answer="Да, можно! Но в команде веселее 🙂",
            ),
        ]
        await faq_repo.save_all(faq_items)

        rules = Rules(
            hackathon_id=saved_hackathon.id,
            content=(
                "Основные правила:\n"
                "1. Уважайте других участников\n"
                "2. Не используйте чужие наработки\n"
                "3. Соблюдайте дедлайны\n"
                "4. Жюри оценивает анекдоты и презентацию\n\n"
                "Критерии:\n"
                "• Смех — 40%\n"
                "• Эстетика — 40%\n"
                "• Реализация — 0%\n"
                "• Презентация — 20%\n"
            ),
        )
        await rules_repo.save(rules)

        participant = User(
            telegram_id=777000111,
            username="demo_participant",
            first_name="Иван",
            last_name="Коляда",
            role=UserRole.PARTICIPANT,
            current_hackathon_id=saved_hackathon.id,
            id=None,
        )
        saved_participant = await user_repo.save(participant)

        organizer = User(
            telegram_id=777000222,
            username="demo_organizer",
            first_name="Анна",
            last_name="Важная",
            role=UserRole.ORGANIZER,
            current_hackathon_id=saved_hackathon.id,
            id=None,
        )
        saved_organizer = await user_repo.save(organizer)

        subscription = ReminderSubscription(
            id=None,
            user_id=saved_participant.id,
            hackathon_id=saved_hackathon.id,
            enabled=True,
        )
        await subscription_repo.save(subscription)

        await session.commit()

        print("OK")
        print("Hackathon:", saved_hackathon.code, saved_hackathon.id)
        print("Participant:", saved_participant.telegram_id)
        print("Organizer:", saved_organizer.telegram_id)


if __name__ == "__main__":
    asyncio.run(setup_demo())
