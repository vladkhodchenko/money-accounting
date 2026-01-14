from typing import Self, Sequence

from sqlalchemy import Table
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from utils.clients.database.base_model import Base


class AbstractModel(Base):
    __table__: Table
    __abstract__ = True

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs) -> Self:
        ...

    @classmethod
    async def update(
            cls,
            session: AsyncSession,
            **kwargs
    ) -> Self:
        ...

    @classmethod
    async def delete(
            cls,
            session: AsyncSession,
            **kwargs
    ) -> None:
        ...

    @classmethod
    async def get(
            cls,
            session: AsyncSession,
            options: tuple[ExecutableOption, ...] | None = None,
            **kwargs
    ) -> Self | None:
        ...

    @classmethod
    async def filter(
            cls,
            session: AsyncSession,
            limit: int | None = None,
            offset: int | None = None,
            options: tuple[ExecutableOption, ...] | None = None,
            order_by = None,
            **kwargs
    ) -> Sequence[Self]:
        ...