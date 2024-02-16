from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import DSN__DATABASE, SYSTEM__DEBUG


engine = create_async_engine(DSN__DATABASE, echo=SYSTEM__DEBUG)
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
