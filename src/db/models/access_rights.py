from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import AbstractModel


class AccessRights(AbstractModel):
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    open_for: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
