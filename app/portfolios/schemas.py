from pydantic import BaseModel
from datetime import date
from app.deposits.logic import Deposit
from typing import Union, List
from app.deposits.consts import Capitalization, TypeBankAccount


class SPortfolio(BaseModel):
    deposits: List[str]
