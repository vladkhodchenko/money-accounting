from pydantic import BaseModel
from typing import Union, List
from consts import Capitalization, TypeBankAccount
from datetime import date


class SDepositCreate(BaseModel):
    name: str
    name_bank: str
    initial_amount: float
    interest_rate: float
    term_months: int
    date_from: Union[date, None] = None
    capitalization_id: Capitalization = Capitalization.MONTHLY
    # type_account: TypeBankAccount = TypeBankAccount.DEPOSIT


class SDepositResponse(SDepositCreate):
    date_to: date
    earned_amount: float
    final_amount: float
