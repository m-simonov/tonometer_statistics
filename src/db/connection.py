from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from db.models.base import AbstractModel


DSN__DATABASE = "sqlite+aiosqlite:///tonometer.db"


engine = create_async_engine(DSN__DATABASE, echo=True)
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session():
    async with async_session() as session:
        yield session
