
from deposits.models import Deposit
from services.base import BaseService

class DepositService(BaseService):
    model = Deposit
