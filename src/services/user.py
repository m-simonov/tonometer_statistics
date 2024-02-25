from aiogram import types
from sqlalchemy.exc import IntegrityError

from db.models.user import User
from db.repositories.access_rights import AccessRightsRepository
from db.repositories.user import UserRepository
from logger import logger
from services.base import AbstractService


class UserService(AbstractService):
    async def add_user(self, message: types.Message):
        try:
            async with self.session.begin():
                await UserRepository(self.session).add(
                    [
                        User(
                            tid=message.from_user.id,
                            username=message.from_user.username,
                            first_name=message.from_user.first_name,
                            last_name=message.from_user.last_name,
                        )
                    ]
                )
                await self.session.commit()
                return True
        except IntegrityError:
            return False

    async def get_users_list(self):
        async with self.session.begin():
            users = await UserRepository(self.session).list()
        text = ""
        for user in users:
            text = text + f"{user.id} - {user.tid} - {user.username} - {user.first_name} - {user.last_name} - {user.date_joined}\n"
        return text

    # @TODO: add sqlalchemy join
    async def get_open_users(self, tid: int):
        async with self.session.begin():
            access_rights = await AccessRightsRepository(self.session).list(
                open_for=tid
            )
            logger.debug("access_rights result", access_rights=[(ar.user, ar.open_for) for ar in access_rights])

            open_users = await UserRepository(self.session).list(
                User.tid.in_([ar.user for ar in access_rights])
            )
            logger.debug("open_users result", open_users=[ou.username for ou in open_users])
        return open_users
