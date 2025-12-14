from dataclasses import dataclass
from typing import Optional
from .ports import UserRepository, RulesRepository
from .dto import RulesDTO


@dataclass
class GetRulesUseCase:
    user_repo: UserRepository
    rules_repo: RulesRepository

    async def execute(self, telegram_id: int) -> Optional[RulesDTO]:
        """Получить правила текущего хакатона userа
        На вход: telegram_id: ID пользователя в tg
        Возвращаем RulesDTO: Правила хакатона или None если не найдены
        """
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if user is None or user.current_hackathon_id is None:
            return None

        rules = await self.rules_repo.get_for_hackathon(user.current_hackathon_id)
        if rules is None:
            return None
        return RulesDTO(content=rules.content)
