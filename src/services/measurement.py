from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import pytz
from logger import logger

from db.models.measurement import Measurement
from db.repositories.measurement import MeasurementRepository
from services.base import AbstractService


@dataclass
class MeasurementData:
    date: datetime.date
    morning: Optional[str]
    afternoon: Optional[str]
    evening: Optional[str]

    def __str__(self) -> str:
        return (
            f"<u>Дата: {self.date}</u>\n"
            f"Утро: <code>{self.morning or '-'}</code>\n"
            f"День: <code>{self.afternoon or '-'}</code>\n"
            f"Вечер: <code>{self.evening or '-'}</code>"
        )


class MeasurementService(AbstractService):
    @staticmethod
    def choose_day_time():
        msk_time = datetime.now(pytz.timezone('Europe/Moscow'))
        hour = int(msk_time.strftime('%H'))
        if 0 < hour < 12:
            column = "morning"
        elif 12 <= hour < 18:
            column = "afternoon"
        else:
            column = "evening"
        return column

    async def get_measurements(self, tid: int, date: datetime.date):
        async with self.session.begin():
            measurement = await MeasurementRepository(self.session).get(user=tid, date=date)
        if measurement:
            return str(MeasurementData(
                date=date,
                morning=measurement.morning,
                afternoon=measurement.afternoon,
                evening=measurement.evening,
            ))
        return "Сегодняшние замеры еще не внесены."

    async def get_month_measurements(self, tid: int, year: int, month: int):
        async with self.session.begin():
            month_measurements = await MeasurementRepository(self.session).get_month_measurements(
                tid,
                year,
                month,
            )

        text = []
        for measurement in month_measurements:
            text.append(str(MeasurementData(
                date=measurement.date,
                morning=measurement.morning,
                afternoon=measurement.afternoon,
                evening=measurement.evening,
            )) + "\n\n")

        if text:
            return ''.join(text)
        return "Замеры в этом месяце еще не вносились."

    async def add_measurement(self, tid: int, date: datetime.date, column: str, value: str):
        async with self.session.begin():
            measurement_repository = MeasurementRepository(self.session)
            measurement = await measurement_repository.get(user=tid, date=date)
            logger.debug(
                "Measurement from DB",
                **{c: getattr(measurement, c) for c in measurement.__table__.columns.keys()} if measurement else None)
            if not measurement:
                item = Measurement(
                    user=tid,
                    date=date,
                )
                setattr(item, column, value)
                await measurement_repository.add([item])
                await self.session.commit()
                logger.debug("A new measurement has been created")
            else:
                setattr(measurement, column, value)
                await self.session.commit()
                logger.debug("The measurement has been updated")
        return f"Результат замера '{value}' записан."
