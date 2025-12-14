from dataclasses import dataclass

from ..domain.models import User, UserRole
from .ports import UserRepository


@dataclass
class StartUserUseCase:
    """Use case для команды /start"""

    user_repo: UserRepository

    async def execute(
        self, telegram_id: int, username: str = "", first_name: str = "", last_name: str = ""
    ) -> User:
        """Зарегистрировать пользователя или обновить его данные
        На вход получаем
            telegram_id: ID пользователя в tg
            username: имя пользователя в tg
            first_name: имя в tg
            last_name: фамилия в tg
        Возвращаем User: Сохраненный пользователь
        """
        user = await self.user_repo.get_by_telegram_id(telegram_id)

        if user is None:
            user = User(
                id=None,
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                role=UserRole.PARTICIPANT,
                current_hackathon_id=None,
            )
        else:
            # Обновляем данные (могло измениться имя)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name

        saved_user = await self.user_repo.save(user)
        return saved_user
