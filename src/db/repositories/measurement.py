from sqlalchemy import extract, select
from db.models.measurement import Measurement
from db.repositories.base import AbstractRepository


class MeasurementRepository(AbstractRepository):
    model = Measurement

    async def get_month_measurements(self, tid: int, year: int, month: int):
        stmt = select(Measurement).filter(
            Measurement.user == tid,
            extract('year', Measurement.date) == year,
            extract('month', Measurement.date) == month,
        )
        month_measurements = await self.session.scalars(stmt)
        return month_measurements
