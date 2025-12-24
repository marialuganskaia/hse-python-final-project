from __future__ import annotations

import asyncio
import os
from datetime import UTC, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

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


def _utc_now_naive() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


async def setup_demo() -> None:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set. Run via docker compose with --env-file .env.docker")

    engine = create_async_engine(database_url)
    Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    now = _utc_now_naive()

    async with Session() as session:
        user_repo = UserRepo(session)
        hackathon_repo = HackathonRepo(session)
        event_repo = EventRepo(session)
        faq_repo = FAQRepo(session)
        rules_repo = RulesRepo(session)
        subscription_repo = SubscriptionRepo(session)

        hackathon_code = "DEMO2025"

        existing = await hackathon_repo.get_by_code(hackathon_code)
        if existing is not None:
            saved_hackathon = existing
        else:
            hackathon = Hackathon(
                id=None,
                code=hackathon_code,
                name="Challenge 2025",
                description="Самый клевый хакатон по питону!",
                start_at=now - timedelta(days=2),
                end_at=now + timedelta(days=4),
                is_active=True,
                location="Вышка, Москва",
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
                answer=(
                    "Все датасеты доступны по ссылке в описании хакатона. "
                    "Нужен VPN для доступа (и чтобы посидеть в запрещенной соцсети)"
                ),
            ),
            FAQItem(
                hackathon_id=saved_hackathon.id,
                question="Можно ли участвовать одному?",
                answer="Да, можно! Но лучше, чтобы у вас был хоть один друг, с которым можно поучаствовать в хакатоне",
            ),
        ]
        await faq_repo.save_all(faq_items)

        # RULES
        rules = Rules(
            hackathon_id=saved_hackathon.id,
            content="""Основные правила:
1. Уважайте других участников
2. Не используйте чужие наработки
3. Соблюдайте дедлайны
4. Жюри оценивает анекдоты и презентацию

Критерии оценивания:
• Смех — 40%
• Эстетическое наслаждение — 40%
• Качество реализации — 0%
• Презентация — 20%""",
        )
        await rules_repo.save(rules)

        # DEMO USERS
        participant_telegram_id = 777000111
        organizer_telegram_id = 777000222

        participant = await user_repo.get_by_telegram_id(participant_telegram_id)
        if participant is None:
            participant = User(
                id=None,
                telegram_id=participant_telegram_id,
                username="demo_participant",
                first_name="Иван",
                last_name="Коляда",
                role=UserRole.PARTICIPANT,
                current_hackathon_id=saved_hackathon.id,
            )
            participant = await user_repo.save(participant)
        else:
            participant.current_hackathon_id = saved_hackathon.id
            participant.role = UserRole.PARTICIPANT
            participant = await user_repo.save(participant)

        organizer = await user_repo.get_by_telegram_id(organizer_telegram_id)
        if organizer is None:
            organizer = User(
                id=None,
                telegram_id=organizer_telegram_id,
                username="demo_organizer",
                first_name="Анна",
                last_name="Важная",
                role=UserRole.ORGANIZER,
                current_hackathon_id=saved_hackathon.id,
            )
            organizer = await user_repo.save(organizer)
        else:
            organizer.current_hackathon_id = saved_hackathon.id
            organizer.role = UserRole.ORGANIZER
            organizer = await user_repo.save(organizer)

        sub = await subscription_repo.get_user_subscription(
            user_id=participant.id, hackathon_id=saved_hackathon.id
        )
        if sub is None:
            sub = ReminderSubscription(
                id=None,
                user_id=participant.id,
                hackathon_id=saved_hackathon.id,
                enabled=True,
            )
        else:
            sub.enabled = True
        await subscription_repo.save(sub)

        # EXTRA USERS + subscriptions
        for i in range(3, 52):
            tg_id = 777000000 + i
            u = await user_repo.get_by_telegram_id(tg_id)
            if u is None:
                u = User(
                    id=None,
                    telegram_id=tg_id,
                    username=f"user_{i}",
                    first_name=f"Участник{i}",
                    last_name="Придуманный",
                    role=UserRole.PARTICIPANT,
                    current_hackathon_id=saved_hackathon.id,
                )
                u = await user_repo.save(u)
            else:
                u.current_hackathon_id = saved_hackathon.id
                u.role = UserRole.PARTICIPANT
                u = await user_repo.save(u)

            if i <= 32:
                s = await subscription_repo.get_user_subscription(
                    user_id=u.id, hackathon_id=saved_hackathon.id
                )
                if s is None:
                    s = ReminderSubscription(
                        id=None,
                        user_id=u.id,
                        hackathon_id=saved_hackathon.id,
                        enabled=True,
                    )
                else:
                    s.enabled = True
                await subscription_repo.save(s)

        await session.commit()

        print("Все ок")
        print(f"Хакатон: {saved_hackathon.name} (ID: {saved_hackathon.id}, code: {saved_hackathon.code})")
        print(f"Участник: @{participant.username} (Telegram ID: {participant.telegram_id})")
        print(f"Организатор: @{organizer.username} (Telegram ID: {organizer.telegram_id})")
        print("Всего пользователей demo-диапазона: 50")
        print("Подписок на уведомления demo-диапазона: 31")
        print(f"Событий в расписании: {len(events)}")
        print(f"Вопросов в FAQ: {len(faq_items)}")


if __name__ == "__main__":
    asyncio.run(setup_demo())
