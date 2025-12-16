from dataclasses import dataclass

from ..domain.models import Hackathon
from .ports import HackathonRepository


@dataclass
class ListHackathonsUseCase:
    """Use case для показа списка активных хакатонов"""

    hackathon_repo: HackathonRepository

    async def execute(self, active_only: bool = True) -> list[Hackathon]:
        """Получить список хакатонов по команде
        На вход active_only: если True, возвращать только активные хакатоны
        Возвращаем List[Hackathon]: Список хакатонов
        """
        if active_only:
            return await self.hackathon_repo.get_all_active()
        else:
            # Если понадобится получить все хакатоны, пока метода нет, на будущее
            return []

