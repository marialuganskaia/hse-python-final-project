from datetime import datetime, timedelta

import pytest

from final_project.src.hackathon_assistant.domain.models import Event, EventType, FAQItem, Hackathon, Rules


class TestCreateHackathonFromConfigUseCase:
    """Тесты для CreateHackathonFromConfigUseCase"""

    @pytest.mark.asyncio
    async def test_create_hackathon_with_all_data(
        self,
        use_case_create_hackathon,
        mock_hackathon_repo,
        mock_event_repo,
        mock_faq_repo,
        mock_rules_repo,
        sample_config,
    ):
        """Создание хакатона со всеми данными: событиями, правилами и FAQ"""
        saved_hackathon = Hackathon(
            id=1,
            name=sample_config["name"],
            code=sample_config["code"],
            description=sample_config["description"],
            start_at=sample_config["start_at"],
            end_at=sample_config["end_at"],
            is_active=sample_config["is_active"],
        )
        mock_hackathon_repo.save.return_value = saved_hackathon

        saved_events = [
            Event(
                id=i,
                hackathon_id=1,
                **{k: v for k, v in event.items() if k != "type"},
                type=event["type"],
            )
            for i, event in enumerate(sample_config["events"], 1)
        ]
        mock_event_repo.save_all.return_value = saved_events

        saved_rules = Rules(id=1, hackathon_id=1, content=sample_config["rules"]["content"])
        mock_rules_repo.save.return_value = saved_rules

        saved_faq_items = [
            FAQItem(id=i, hackathon_id=1, question=item["question"], answer=item["answer"])
            for i, item in enumerate(sample_config["faq"], 1)
        ]
        mock_faq_repo.save_all.return_value = saved_faq_items

        result = await use_case_create_hackathon.execute(sample_config)

        mock_hackathon_repo.save.assert_called_once()

        hackathon_arg = mock_hackathon_repo.save.call_args[0][0]
        assert hackathon_arg.name == "Test Hackathon 2024"
        assert hackathon_arg.code == "TEST2024"
        assert hackathon_arg.description == "Test description"
        assert hackathon_arg.is_active is True
        assert hackathon_arg.id is None

        mock_event_repo.save_all.assert_called_once()
        events_arg = mock_event_repo.save_all.call_args[0][0]
        assert len(events_arg) == 2
        assert events_arg[0].title == "Opening Ceremony"
        assert events_arg[0].hackathon_id == 1
        assert events_arg[0].type == EventType.OTHER
        assert events_arg[1].title == "Workshop"
        assert events_arg[1].type == EventType.LECTURE

        mock_rules_repo.save.assert_called_once()
        rules_arg = mock_rules_repo.save.call_args[0][0]
        assert rules_arg.hackathon_id == 1
        assert rules_arg.content == "1. Be respectful\n2. No cheating\n3. Have fun!"

        mock_faq_repo.save_all.assert_called_once()
        faq_arg = mock_faq_repo.save_all.call_args[0][0]
        assert len(faq_arg) == 2
        assert faq_arg[0].question == "What is the team size?"
        assert faq_arg[0].answer == "2-5 people per team"
        assert faq_arg[0].hackathon_id == 1

        assert result == saved_hackathon
        assert result.id == 1

    @pytest.mark.asyncio
    async def test_create_hackathon_with_events_only(
        self,
        use_case_create_hackathon,
        mock_hackathon_repo,
        mock_event_repo,
        mock_faq_repo,
        mock_rules_repo,
    ):
        """Создание хакатона только с событиями"""
        now = datetime.now()
        config = {
            "name": "Events Only Hackathon",
            "code": "EVENTS2024",
            "start_at": now,
            "end_at": now + timedelta(days=2),
            "is_active": False,
            "events": [
                {
                    "title": "Only Event",
                    "type": EventType.CHECKPOINT,
                    "starts_at": now + timedelta(hours=1),
                    "ends_at": now + timedelta(hours=2),
                }
            ],
        }

        saved_hackathon = Hackathon(
            id=1,
            name=config["name"],
            code=config["code"],
            description="",
            start_at=config["start_at"],
            end_at=config["end_at"],
            is_active=False,
        )
        mock_hackathon_repo.save.return_value = saved_hackathon

        saved_event = Event(
            id=1,
            hackathon_id=1,
            title="Only Event",
            type=EventType.CHECKPOINT,
            starts_at=config["events"][0]["starts_at"],
            ends_at=config["events"][0]["ends_at"],
            location=None,
            description=None,
        )
        mock_event_repo.save_all.return_value = [saved_event]

        result = await use_case_create_hackathon.execute(config)

        mock_hackathon_repo.save.assert_called_once()
        mock_event_repo.save_all.assert_called_once()
        mock_rules_repo.save.assert_not_called()
        mock_faq_repo.save_all.assert_not_called()

        events_arg = mock_event_repo.save_all.call_args[0][0]
        assert len(events_arg) == 1
        assert events_arg[0].title == "Only Event"
        assert events_arg[0].type == EventType.CHECKPOINT
        assert events_arg[0].location is None
        assert events_arg[0].description is None

        assert result.id == 1
        assert result.is_active is False

    @pytest.mark.asyncio
    async def test_create_hackathon_empty_events_list(
        self,
        use_case_create_hackathon,
        mock_hackathon_repo,
        mock_event_repo,
        mock_faq_repo,
        mock_rules_repo,
    ):
        """Создание хакатона с пустым списком событий"""
        now = datetime.now()
        config = {
            "name": "Empty Events Hackathon",
            "code": "EMPTY2024",
            "start_at": now,
            "end_at": now + timedelta(days=1),
            "events": [],
            "rules": {"content": "Test rules"},
            "faq": [],
        }

        saved_hackathon = Hackathon(
            id=1,
            name=config["name"],
            code=config["code"],
            description="",
            start_at=config["start_at"],
            end_at=config["end_at"],
            is_active=True,
        )
        mock_hackathon_repo.save.return_value = saved_hackathon

        saved_rules = Rules(id=1, hackathon_id=1, content=config["rules"]["content"])
        mock_rules_repo.save.return_value = saved_rules

        result = await use_case_create_hackathon.execute(config)

        mock_hackathon_repo.save.assert_called_once()
        mock_rules_repo.save.assert_called_once()

        mock_event_repo.save_all.assert_not_called()
        mock_faq_repo.save_all.assert_not_called()

        assert result.id == 1
