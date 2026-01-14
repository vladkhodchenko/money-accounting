import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from utils.clients.database.base_model import Base


DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


async def get_database_session_sqlite() -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(f"sqlite+aiosqlite:///onlycash.db")
    return async_sessionmaker(bind=engine, expire_on_commit=False)

async def create_database_sqlite():
    engine = create_async_engine(f"sqlite+aiosqlite:///onlycash.db")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def create_database():
    engine = create_async_engine(settings.database_url, echo=True, future=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_database_engine() -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(settings.database_url, echo=True, future=True)

    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)