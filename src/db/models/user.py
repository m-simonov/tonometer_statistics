from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import AbstractModel


class User(AbstractModel):
    tid: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=True)
    username: Mapped[str] = mapped_column(String(32), unique=True)
    first_name: Mapped[str] = mapped_column(String(32), nullable=True)
    last_name: Mapped[str] = mapped_column(String(32), nullable=True)
