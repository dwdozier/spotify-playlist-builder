from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
from backend.app.core.config import settings

# Use pool_pre_ping to handle dropped connections (common in cloud environments)
engine = create_async_engine(str(settings.DATABASE_URL), pool_pre_ping=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
