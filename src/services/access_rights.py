from db.models.user import User
from db.repositories.access_rights import AccessRightsRepository
from db.models.access_rights import AccessRights
from db.repositories.user import UserRepository
from services.base import AbstractService


class AccessRightsService(AbstractService):
    async def open_access(self, user: int, open_for: str):
        async with self.session.begin():
            trusted_user = await UserRepository(self.session).get(
                (User.tid == open_for) | (User.username == open_for)
            )
            if not trusted_user:
                return (
                    f'Не удалось открыть доступ пользователю "{open_for}".\n'
                    'Возможные причины:\n'
                    '1. Такого пользователя не существует\n'
                    f'2. "{open_for}" не является пользователем бота\n'
                    '3. Вы ввели неверный юзернейм'
                )

            is_duplication = await AccessRightsRepository(self.session).get(
                user=user,
                open_for=trusted_user.tid,
            )
            if is_duplication:
                return f'{open_for} уже добавлен в список доверенных пользователей'

            await AccessRightsRepository(self.session).add(
                [
                    AccessRights(
                        user=user,
                        open_for=trusted_user.tid,
                    )
                ]
            )
        return (
            "Результаты ваших замеров теперь доступны "
            f"пользователю {open_for}"
        )
