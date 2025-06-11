from pydantic import BaseModel
from datetime import date
from models import Deposit
from enum import Enum
from typing import Union, List


class Capitalization(str, Enum):
    monthly = "monthly"
    daily = "daily"
    end = "end"


class DepositCreate(BaseModel):
    name: str
    initial_amount: float
    interest_rate: float
    term_months: int
    date_from: Union[date, None] = date
    capitalization: Capitalization = Capitalization.monthly


class DepositResponse(DepositCreate):
    date_to: date
    profit: float
    total_amount: float


class Portfolio(BaseModel):
    deposits: List[str]
