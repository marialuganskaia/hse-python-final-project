import asyncio
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.hackathon_assistant.adapters.db.models import Base
from src.hackathon_assistant.adapters.db.repositories import (
    UserRepo, HackathonRepo, EventRepo, FAQRepo, RulesRepo, SubscriptionRepo
)
from src.hackathon_assistant.domain.models import (
    User, Hackathon, Event, FAQItem, Rules, ReminderSubscription,
    UserRole, EventType
)


async def setup_demo():
    engine = create_async_engine("sqlite+aiosqlite:///demo.db")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with Session() as session:
        user_repo = UserRepo(session)
        hackathon_repo = HackathonRepo(session)
        event_repo = EventRepo(session)
        faq_repo = FAQRepo(session)
        rules_repo = RulesRepo(session)
        subscription_repo = SubscriptionRepo(session)

        hackathon = Hackathon(
            code="demohack",
            name="Challenge 2025",
            description="Самый клевый хакатон по питону!",
            start_at=datetime.now() - timedelta(days=2),
            end_at=datetime.now() + timedelta(days=4),
            is_active=True,
            location="Вышка, Москва"
        )
        saved_hackathon = await hackathon_repo.save(hackathon)

        events = [
            Event(
                hackathon_id=saved_hackathon.id,
                title="Регистрация и кофе-брейк",
                type=EventType.MEETUP,
                starts_at=datetime.now() - timedelta(hours=3),
                ends_at=datetime.now() - timedelta(hours=1),
                location="1 этаж",
                description="Еда, кофе, знакомство"
            ),
            Event(
                hackathon_id=saved_hackathon.id,
                title="Чекпоинт 1: Идея",
                type=EventType.CHECKPOINT,
                starts_at=datetime.now() + timedelta(minutes=20),
                ends_at=datetime.now() + timedelta(hours=1),
                location="Атриум",
                description="Представьте идеи"
            ),
            Event(
                hackathon_id=saved_hackathon.id,
                title="Лекция: как с помощью питона зарабатывать много денег",
                type=EventType.LECTURE,
                starts_at=datetime.now() + timedelta(hours=3),
                ends_at=datetime.now() + timedelta(hours=4),
                location="R308",
                description="Разбираем реальные кейсы"
            ),
            Event(
                hackathon_id=saved_hackathon.id,
                title="Сдача проектов",
                type=EventType.DEADLINE,
                starts_at=datetime.now() + timedelta(days=1, hours=10),
                ends_at=datetime.now() + timedelta(days=1, hours=12),
                location="Онлайн-форма",
                description="Дедлайн подачи проектов"
            )
        ]
        await event_repo.save_all(events)


        faq_items = [
            FAQItem(
                hackathon_id=saved_hackathon.id,
                question="Как подать проект?",
                answer="Проекты подаются через онлайн-форму. Ссылка появится за час до дедлайна"
            ),
            FAQItem(
                hackathon_id=saved_hackathon.id,
                question="Где взять доступ к данным?",
                answer="Все датасеты доступны по ссылке в описании хакатона. Нужен VPN для доступ (и чтобы посидеть в запрещенной соцсети)"
            ),
            FAQItem(
                hackathon_id=saved_hackathon.id,
                question="Можно ли участвовать одному?",
                answer="Да, можно! Но лучше, чтобы у вас был хоть один друг, с которым можно поучаствовать в хакатоне"
            )
        ]
        await faq_repo.save_all(faq_items)

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
            • Презентация — 20%"""
        )
        await rules_repo.save(rules)

        participant = User(
            telegram_id=777000111,
            username="demo_participant",
            first_name="Иван",
            last_name="Коляда",
            role=UserRole.PARTICIPANT,
            current_hackathon_id=saved_hackathon.id
        )
        saved_participant = await user_repo.save(participant)

        organizer = User(
            telegram_id=777000222,
            username="demo_organizer",
            first_name="Анна",
            last_name="Важная",
            role=UserRole.ORGANIZER,
            current_hackathon_id=saved_hackathon.id
        )
        saved_organizer = await user_repo.save(organizer)

        subscription = ReminderSubscription(
            user_id=saved_participant.id,
            hackathon_id=saved_hackathon.id,
            enabled=True
        )
        await subscription_repo.save(subscription)

        for i in range(3, 52):  # 49 дополнительных участников
            virtual_user = User(
                telegram_id=777000000 + i,
                username=f"user_{i}",
                first_name=f"Участник{i}",
                last_name="Придуманный",
                role=UserRole.PARTICIPANT,
                current_hackathon_id=saved_hackathon.id
            )
            saved_virtual = await user_repo.save(virtual_user)

            if i <= 32:
                sub = ReminderSubscription(
                    user_id=saved_virtual.id,
                    hackathon_id=saved_hackathon.id,
                    enabled=True
                )
                await subscription_repo.save(sub)

        await session.commit()

        print("Все оки")
        print(f"Хакатон: {saved_hackathon.name} (ID: {saved_hackathon.id})")
        print(f"Участник: @{saved_participant.username} (Telegram ID: {saved_participant.telegram_id})")
        print(f"Организатор: @{saved_organizer.username} (Telegram ID: {saved_organizer.telegram_id})")
        print(f"Всего участников: 50")
        print(f"Подписок на уведомления: 31")
        print(f"Событий в расписании: {len(events)}")
        print(f"Вопросов в FAQ: {len(faq_items)}")


if __name__ == "__main__":
    asyncio.run(setup_demo())