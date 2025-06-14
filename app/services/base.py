from database import session
from deposits.models import Deposit
from sqlalchemy import select


class BaseService:
    model = None

    @classmethod
    def find_by_id(cls, model_id: int):
        with session() as s:
            query = select(cls.model).filter_by(id=model_id)
            result = s.execute(query)
            return result.scalars().one_or_none()

    @classmethod
    def find_one_or_none(cls, **filter_by):
        with session() as s:
            query = select(cls.model).filter_by(**filter_by)
            result = s.execute(query)
            return result.scalars().one_or_none()

    @classmethod
    def find_all(cls, **filter_by):
        with session() as s:
            query = select(cls.model).filter_by(**filter_by)
            result = s.execute(query)
            return result.scalars().all()
