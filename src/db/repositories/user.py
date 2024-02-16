from db.models.user import User
from db.repositories.base import AbstractRepository


class UserRepository(AbstractRepository):
    model = User
