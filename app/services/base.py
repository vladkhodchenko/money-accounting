from database import session
from deposits.models import Deposit
from sqlalchemy import select


class BaseService:
    model = None

    @classmethod
    def find_all(cls):
        with session() as s:
            query = select(cls.model)
            result = s.execute(query)
            return result.scalars().all()
