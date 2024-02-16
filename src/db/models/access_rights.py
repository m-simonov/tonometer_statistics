from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import AbstractModel


class AccessRights(AbstractModel):
    user: Mapped[int] = mapped_column(ForeignKey('user.tid'), nullable=False)
    open_for: Mapped[int] = mapped_column(ForeignKey('user.tid'), nullable=False)
