from services.models.deposits import Deposit
from services.database.base import BaseService


class DepositService(BaseService):
    model = Deposit
