from sqlalchemy import extract, select, func
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
        return await self.session.scalars(stmt)

    async def count_month_measurements(self, tid: int, year: int, month: int):
        stmt = select(func.count(Measurement.id)).filter(
            Measurement.user == tid,
            extract('year', Measurement.date) == year,
            extract('month', Measurement.date) == month,
        )
        return await self.session.scalar(stmt)

    async def count_months_measurements_all(self, tid: int, year: int):
        stmt = select(
            extract('month', Measurement.date).label('month'),
            func.count(Measurement.id).label('count'),
        ).filter(
            Measurement.user == tid,
            extract('year', Measurement.date) == year,
        ).group_by(
            extract('month', Measurement.date),
        )
        result = await self.session.execute(stmt)
        return [r._asdict() for r in result]
