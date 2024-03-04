import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from db.models.base import AbstractModel


class Feedback(AbstractModel):
    user: Mapped[int] = mapped_column(ForeignKey('user.tid'))
    text: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
