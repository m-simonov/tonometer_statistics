from datetime import datetime

import pytz

from db.models.measurement import Measurement
from db.repositories.measurement import MeasurementRepository
from services.base import AbstractService


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
            return (
                f"Дата: {date}\n\n"
                f"Утро: {measurement.morning or '-'}\n"
                f"День: {measurement.afternoon or '-'}\n"
                f"Вечер: {measurement.evening or '-'}"
            )
        return "Сегодняшние замеры еще не внесены."

    async def get_month_measurements(self, tid: int, year: int, month: int):
        async with self.session.begin():
            month_meterings = await MeasurementRepository(self.session).get_month_meterings(
                tid,
                year,
                month,
            )

        text = []
        for metering in month_meterings:
            text.append(
                f"Дата: {metering.date}\n"
                f"Утро: {metering.morning}\n"
                f"День: {metering.afternoon}\n"
                f"Вечер: {metering.evening}\n\n"
            )

        if text:
            return ''.join(text)
        return "Замеры в этом месяце еще не вносились."

    async def add_measurement(self, tid: int, date: datetime.date, column: str, value: str):
        async with self.session.begin():
            measurement = await MeasurementRepository(self.session).get(user=tid, date=date)
            is_added = getattr(measurement, column) if measurement else None
            if not is_added:
                item = Measurement(
                    user=tid,
                    date=date,
                )
                setattr(item, column, value)
                await MeasurementRepository(self.session).add([item])
                await self.session.commit()
            else:
                setattr(measurement, column, value)
                await self.session.commit()
        return f"Результат замера '{value}' записан."
