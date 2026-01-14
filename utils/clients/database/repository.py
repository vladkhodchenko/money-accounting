from sqlalchemy.ext.asyncio import AsyncSession
from utils.clients.database.mixin_model import MixinModel


class BasePostgresRepository:
    model: type[MixinModel]

    def __init__(self, session: AsyncSession):
        self.session = session


class BaseSqliteRepository:
    model: type[MixinModel]

    def __init__(self, session: AsyncSession):
        self.session = session