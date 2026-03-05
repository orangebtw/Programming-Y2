from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

DATABASE_URL = "sqlite+aiosqlite:///./database.db"

engine = create_async_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
