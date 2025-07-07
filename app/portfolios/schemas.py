from pydantic import BaseModel
from datetime import date
from logic import Deposit
from typing import Union, List
from consts import Capitalization, TypeBankAccount


class SPortfolio(BaseModel):
    deposits: List[str]
