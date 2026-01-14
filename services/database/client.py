from sqlalchemy.ext.asyncio import AsyncSession

from utils.clients.database.engine import get_database_engine


async def get_database_session() -> AsyncSession:
    async_session = await get_database_engine()

    async with async_session() as session:
        yield session