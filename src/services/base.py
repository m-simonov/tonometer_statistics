from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from db.connection import async_session_maker


class AbstractService:
    def __init__(self, session: Optional[AsyncSession] = async_session_maker()):
        self.session = session
