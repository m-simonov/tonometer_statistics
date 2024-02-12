from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


DSN__DATABASE = "sqlite+aiosqlite:///tonometer.db"


engine = create_async_engine(DSN__DATABASE, echo=True)
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
