from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import (
    date, 
    datetime,
)

from consts import Capitalization, TypeBankAccount

class SDepositCreate(BaseModel):
    name: str
    name_bank: str
    initial_amount: float
    interest_rate: float
    term_months: int
    date_from: Union[date, None] = None
    capitalization_id: Capitalization = Capitalization.MONTHLY
    # type_account: TypeBankAccount = TypeBankAccount.DEPOSIT
    
class SDeposit(SDepositCreate):
    date_to: date
    earned_amount: float
    final_amount: float
    
    class Config:
        orm_mode = True
        exclude = {"created_at", "updated_at"}

class SDepositPatch(BaseModel):
    name: Optional[str] = None
    name_bank: Optional[str] = None
    initial_amount: Optional[float] = None
    interest_rate: Optional[float] = None
    term_months: Optional[int] = None
    date_from: Optional[date] = None
    capitalization_id: Optional[Capitalization] = Capitalization.MONTHLY
    #type_account: Optional[TypeBankAccount] = TypeBankAccount.DEPOSIT
