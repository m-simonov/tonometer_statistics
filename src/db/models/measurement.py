import datetime

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import UniqueConstraint

from db.models.base import AbstractModel


class Measurement(AbstractModel):
    user: Mapped[int] = mapped_column(ForeignKey('user.tid'))
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    morning: Mapped[str] = mapped_column(String(11), nullable=True)
    afternoon: Mapped[str] = mapped_column(String(11), nullable=True)
    evening: Mapped[str] = mapped_column(String(11), nullable=True)

    __table_args__ = (
        UniqueConstraint('user', 'date', name='unique_user_date'),
    )
