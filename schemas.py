from pydantic import BaseModel
from datetime import date
from models import Deposit
from typing import Union, List
from consts import Capitalization


class SDepositCreate(BaseModel):
    name: str
    initial_amount: float
    interest_rate: float
    term_months: int
    date_from: Union[date, None] = date
    capitalization: Capitalization = Capitalization.MONTHLY


class SDepositResponse(SDepositCreate):
    date_to: date
    profit: float
    total_amount: float


class SPortfolio(BaseModel):
    deposits: List[str]
