from datetime import datetime
from typing import Optional
from sqlalchemy.exc import IntegrityError

from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession

from db.connection import async_session_maker
from db.models.user import User
from db.repositories.user import UserRepository
from db.repositories.measurement import MeasurementRepository


class MeasurementService:
    def __init__(self) -> None:
        self.session: Optional[AsyncSession] = async_session_maker()

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
                self.session.commit()
                return True
        except IntegrityError:
            return False

    async def get_today_meterings(self, user: str, date: datetime.date):
        async with self.session.begin():
            measurement = await MeasurementRepository(self.session).get(user=user, date=date)
        if measurement:
            return (
                f"Дата: {date}\n\n"
                f"Утро: {measurement.morning}\n"
                f"День: {measurement.afternoon}\n"
                f"Вечер: {measurement.evening}"
            )
        return "Сегодняшние замеры еще не внесены"
