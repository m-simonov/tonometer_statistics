from typing import Optional

from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession

from db.connection import async_session_maker
from db.models.user import User
from db.repositories.user import UserRepository


class MeasurementService:

    def __init__(self) -> None:
        self.session: Optional[AsyncSession] = async_session_maker()

    async def add_user(self, message: types.Message):
        async with self.session.begin():
            user_repository = UserRepository(self.session)
            await user_repository.add(
                [
                    User(
                        tid=message.from_user.id,
                        username=message.from_user.username,
                        first_name=message.from_user.first_name,
                        last_name=message.from_user.last_name,
                    )
                ]
            )
            self.session.commit()
