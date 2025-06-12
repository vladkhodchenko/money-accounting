from pydantic import BaseModel
from datetime import date
from logic import Deposit
from typing import Union, List
from consts import Capitalization, TypeBankAccount


class SDepositCreate(BaseModel):
    name: str
    name_bank: str
    initial_amount: float
    interest_rate: float
    term_months: int
    date_from: Union[date, None] = None
    capitalization: Capitalization = Capitalization.MONTHLY
    type_account: TypeBankAccount = TypeBankAccount.DEPOSIT


class SDepositResponse(SDepositCreate):
    date_to: date
    profit: float
    total_amount: float


class SPortfolio(BaseModel):
    deposits: List[str]
