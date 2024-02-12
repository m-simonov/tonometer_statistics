from db.models.access_rights import AccessRights
from db.repositories.base import AbstractRepository


class UserRepository(AbstractRepository):
    model = AccessRights
