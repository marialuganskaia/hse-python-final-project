from dataclasses import dataclass
from typing import List
from .ports import UserRepository, FAQRepository
from .dto import FAQItemDTO


@dataclass
class GetFAQUseCase:
    user_repo: UserRepository
    faq_repo: FAQRepository

    async def execute(self, telegram_id: int) -> List[FAQItemDTO]:
        """Получить FAQ текущего хакатона userа
        На вход: telegram_id: ID пользователя в tg
        Возвращаем List[FAQItemDTO]: список вопросов-ответов
        """
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if user is None or user.current_hackathon_id is None:
            return []
        faq_items = await self.faq_repo.get_by_hackathon(user.current_hackathon_id)
        return [
            FAQItemDTO(
                question=item.question,
                answer=item.answer)
            for item in faq_items
        ]
