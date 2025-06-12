from database import session
from deposits.models import Deposit
from sqlalchemy import select

class DepositService:
    @classmethod
    def find_all(cls):
        with session() as s:
            query = select(Deposit)
            deposits = s.execute(query)
            return deposits.scalars().all()