from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.base import AbstractModel


class AbstractRepository:
    model = AbstractModel

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, batch: List[model]):
        self.session.add_all(batch)

    async def get(self, *args, **kwargs):
        if args:
            stmt = select(self.model).filter(*args)
        elif kwargs:
            stmt = select(self.model).filter_by(**kwargs)
        else:
            raise ValueError
        result = await self.session.scalar(stmt)
        return result

    async def list(self, *args, **kwargs):
        stmt = select(self.model)
        if args:
            stmt = stmt.filter(*args)
        else:
            stmt = stmt.filter_by(**kwargs)
        result = await self.session.scalars(stmt)
        return result.all()
