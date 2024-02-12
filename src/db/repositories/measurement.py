from db.models.measurement import Measurement
from db.repositories.base import AbstractRepository


class UserRepository(AbstractRepository):
    model = Measurement
