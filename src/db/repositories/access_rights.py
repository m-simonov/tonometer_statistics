from db.models.access_rights import AccessRights
from db.repositories.base import AbstractRepository


class AccessRightsRepository(AbstractRepository):
    model = AccessRights
