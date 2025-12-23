import argparse
import json
from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, call, patch

import pytest

from hackathon_assistant.domain.models import EventType, Hackathon
from hackathon_assistant.infra.cli import _parse_dt, _normalize_config, CLI


def test_cli_parser():
    """Тест парсера CLI"""

    cli = CLI()
    parser = cli.build_parser()

    # Проверяем что команды добавлены
    assert "db-ping" in parser.format_help()
    assert "create-hackathon" in parser.format_help()


@pytest.mark.asyncio
async def test_cli_db_ping_success():
    """Тест команды db-ping (успех)"""

    cli = CLI()

    # Создаем мок для настроек
    mock_settings = MagicMock()
    mock_settings.database_url = "test://database"

    with patch("hackathon_assistant.infra.cli.get_settings", return_value=mock_settings):
        with patch("hackathon_assistant.infra.cli.db_ping", AsyncMock(return_value=True)):
            with patch("builtins.print") as mock_print:
                args = argparse.Namespace()
                result = await cli._cmd_db_ping(args)

                assert result == 0
                # Проверяем ВСЕ вызовы print
                mock_print.assert_has_calls(
                    [call(f"DATABASE_URL={mock_settings.database_url}"), call("DB ping OK")]
                )


@pytest.mark.asyncio
async def test_cli_db_ping_failure():
    """Тест команды db-ping (ошибка)"""

    cli = CLI()

    # Создаем мок для настроек
    mock_settings = MagicMock()
    mock_settings.database_url = "test://database"

    with patch("hackathon_assistant.infra.cli.get_settings", return_value=mock_settings):
        with patch("hackathon_assistant.infra.cli.db_ping", AsyncMock(return_value=False)):
            with patch("builtins.print") as mock_print:
                args = argparse.Namespace()
                result = await cli._cmd_db_ping(args)

                assert result == 2
                mock_print.assert_has_calls(
                    [call(f"DATABASE_URL={mock_settings.database_url}"), call("DB ping failed")]
                )


def test_normalize_config():
    """Тест нормализации конфига"""

    data = {
        "hackathon": {
            "name": "Test",
            "code": "TEST",
            "start_at": "2025-01-01T10:00:00Z",
            "end_at": "2025-01-02T10:00:00Z",
        },
        "events": [
            {
                "title": "Event 1",
                "type": "checkpoint",
                "starts_at": "2025-01-01T11:00:00Z",
                "ends_at": "2025-01-01T12:00:00Z",
            }
        ],
        "rules": {"content": "Rules"},
        "faq": [{"question": "Q?", "answer": "A"}],
    }

    result = _normalize_config(data)

    assert result["name"] == "Test"
    assert result["code"] == "TEST"
    assert isinstance(result["start_at"], datetime)
    assert isinstance(result["end_at"], datetime)
    assert len(result["events"]) == 1
    assert result["events"][0]["type"] == EventType.CHECKPOINT


def test_normalize_config_flat():
    """Тест нормализации плоского конфига"""

    data = {
        "name": "Test",
        "code": "TEST",
        "start_at": "2025-01-01T10:00:00Z",
        "end_at": "2025-01-02T10:00:00Z",
        "events": [],
        "faq": [],
    }

    result = _normalize_config(data)

    assert result["name"] == "Test"
    assert result["code"] == "TEST"
    assert isinstance(result["start_at"], datetime)
    assert isinstance(result["end_at"], datetime)


def test_parse_dt():
    """Тест парсинга даты"""

    dt_str = "2025-01-01T10:00:00"
    result = _parse_dt(dt_str, "test")
    assert isinstance(result, datetime)
    assert result.year == 2025
    assert result.month == 1
    assert result.day == 1

    dt_obj = datetime.now()
    result = _parse_dt(dt_obj, "test")
    assert result == dt_obj

    dt_with_z = "2025-01-01T10:00:00Z"
    result = _parse_dt(dt_with_z, "test")
    assert isinstance(result, datetime)


@pytest.mark.asyncio
async def test_create_hackathon_success():
    """Тест успешного создания хакатона"""

    cli = CLI()

    # Создаем временный JSON файл
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        config = {
            "name": "Test Hackathon",
            "code": "TEST2025",
            "start_at": "2025-01-01T10:00:00Z",
            "end_at": "2025-01-02T10:00:00Z",
        }
        json.dump(config, f)
        config_path = Path(f.name)

    try:
        # Мокаем все зависимости
        with patch("hackathon_assistant.infra.cli.get_session") as mock_session:
            with patch("hackathon_assistant.infra.cli.RepositoryProvider") as mock_repo:
                # Настраиваем моки
                mock_session_instance = AsyncMock()
                mock_session.return_value.__aenter__.return_value = mock_session_instance

                mock_repo_instance = mock_repo.return_value
                mock_hackathon_repo = AsyncMock()
                mock_hackathon_repo.get_by_code.return_value = None  # хакатон не существует
                saved_hackathon = MagicMock()
                saved_hackathon.id = 1
                saved_hackathon.code = "TEST2025"
                saved_hackathon.name = "Test Hackathon"
                mock_hackathon_repo.save.return_value = saved_hackathon
                mock_repo_instance.hackathon_repo.return_value = mock_hackathon_repo

                # Мокаем другие репозитории
                mock_repo_instance.event_repo.return_value = AsyncMock()
                mock_repo_instance.faq_repo.return_value = AsyncMock()
                mock_repo_instance.rules_repo.return_value = AsyncMock()

                with patch("builtins.print") as mock_print:
                    # Создаем аргументы
                    args = MagicMock()
                    args.config = config_path

                    result = await cli._cmd_create_hackathon(args)

                    assert result == 0  # успех
                    mock_print.assert_called_with(
                        "Created hackathon id=1 code='TEST2025' name='Test Hackathon'"
                    )
    finally:
        # Удаляем временный файл
        config_path.unlink()


@pytest.mark.asyncio
async def test_create_hackathon_already_exists():
    """Тест создания хакатона который уже существует"""

    cli = CLI()

    # Создаем временный JSON файл
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        config = {
            "name": "Test Hackathon",
            "code": "TEST2025",
            "start_at": "2025-01-01T10:00:00Z",
            "end_at": "2025-01-02T10:00:00Z",
        }
        json.dump(config, f)
        config_path = Path(f.name)

    try:
        with patch("hackathon_assistant.infra.cli.get_session") as mock_session:
            with patch("hackathon_assistant.infra.cli.RepositoryProvider") as mock_repo:
                mock_session_instance = AsyncMock()
                mock_session.return_value.__aenter__.return_value = mock_session_instance

                mock_repo_instance = mock_repo.return_value
                mock_hackathon_repo = AsyncMock()
                # Хакатон уже существует
                existing_hackathon = Hackathon(
                    id=1,
                    code="TEST2025",
                    name="Existing Hackathon",
                    start_at=datetime.now(),
                    end_at=datetime.now(),
                )
                mock_hackathon_repo.get_by_code.return_value = existing_hackathon
                mock_repo_instance.hackathon_repo.return_value = mock_hackathon_repo

                with patch("builtins.print") as mock_print:
                    args = MagicMock()
                    args.config = config_path

                    result = await cli._cmd_create_hackathon(args)

                    assert result == 0
                    # Проверяем что выведено сообщение о существующем хакатоне
                    assert any("already exists" in str(call) for call in mock_print.call_args_list)
    finally:
        config_path.unlink()


def test_main_function():
    """Тест основной функции CLI"""
    from hackathon_assistant.infra.cli import main

    # Тестируем с аргументами командной строки
    with patch("sys.argv", ["cli.py", "db-ping"]):
        with patch("hackathon_assistant.infra.cli.CLI.run") as mock_run:
            mock_run.return_value = 0
            result = main(["db-ping"])

            assert result == 0
            mock_run.assert_called_once_with(["db-ping"])
