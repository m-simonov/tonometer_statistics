import datetime

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import AbstractModel


class Measurement(AbstractModel):
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    morning: Mapped[str] = mapped_column(String(11))
    afternoon: Mapped[str] = mapped_column(String(11))
    evening: Mapped[str] = mapped_column(String(11))
