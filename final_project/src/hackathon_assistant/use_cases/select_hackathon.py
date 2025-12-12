from dataclasses import dataclass
from typing import Optional
from .ports import UserRepository, HackathonRepository
from ..domain.models import Hackathon


@dataclass
class SelectHackathonByCodeUseCase:
    """
    Use case для выбора хакатона по коду
    Используется когда пользователь:
    1) Переходит по ссылке t.me/bot?start=CODE
    2) вводит код после регистрации
    """
    user_repo: UserRepository
    hackathon_repo: HackathonRepository

    async def execute(self, telegram_id: int, hackathon_code: str) -> Optional[Hackathon]:
        """Привязка пользователя к хакатону по коду
        На вход
            telegram_id: ID пользователя в tg
            hackathon_code: код хакатона
        Возвращаем
            Hackathon: если хакатон найден и привязан
            None: если хакатон не найден или пользователь не существует
        """
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if user is None:
            return None

        hackathon = await self.hackathon_repo.get_by_code(hackathon_code)
        if hackathon is None:
            return None

        user.current_hackathon_id = hackathon.id
        await self.user_repo.save(user)
        return hackathon
