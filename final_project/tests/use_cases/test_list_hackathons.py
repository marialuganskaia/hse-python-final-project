from dataclasses import replace

import pytest

from hackathon_assistant.use_cases.list_hackathons import ListHackathonsUseCase


class TestListHackathonsUseCase:
    """Тесты для ListHackathonsUseCase."""

    @pytest.mark.asyncio
    async def test_execute_active_only(self, mock_hackathon_repo, sample_hackathon):
        """Тест получения активных хакатонов."""
        another_hackathon = replace(sample_hackathon, id=2, code="HACK2023")
        another_hackathon.id = 2
        another_hackathon.code = "HACK2025"
        another_hackathon.is_active = True

        inactive_hackathon = replace(sample_hackathon, id=3, code="HACK2022", is_active=False)
        inactive_hackathon.id = 3
        inactive_hackathon.code = "INACTIVE"
        inactive_hackathon.is_active = False

        mock_hackathon_repo.get_all_active.return_value = [sample_hackathon, another_hackathon]

        use_case = ListHackathonsUseCase(hackathon_repo=mock_hackathon_repo)

        result = await use_case.execute(active_only=True)

        mock_hackathon_repo.get_all_active.assert_called_once()
        assert len(result) == 2
        assert all(h.is_active for h in result)
        assert result[0].code == "HACK2024"
        assert result[1].code == "HACK2025"

    @pytest.mark.asyncio
    async def test_execute_all_hackathons(self, mock_hackathon_repo):
        """Тест получения всех хакатонов (включая неактивные)."""
        mock_hackathon_repo.get_all_active.return_value = []

        use_case = ListHackathonsUseCase(hackathon_repo=mock_hackathon_repo)

        result = await use_case.execute(active_only=False)

        mock_hackathon_repo.get_all_active.assert_not_called()
        assert result == []

    @pytest.mark.asyncio
    async def test_execute_no_hackathons(self, mock_hackathon_repo):
        """Тест получения списка, когда нет активных хакатонов."""
        mock_hackathon_repo.get_all_active.return_value = []

        use_case = ListHackathonsUseCase(hackathon_repo=mock_hackathon_repo)

        result = await use_case.execute(active_only=True)

        mock_hackathon_repo.get_all_active.assert_called_once()
        assert result == []
