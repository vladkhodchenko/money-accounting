from pydantic import BaseModel, Field, validator
from typing import Union, List, Optional
from datetime import (
    date,
    datetime,
)

from deposits.consts import Capitalization, TypeBankAccount


class SDepositCreate(BaseModel):
    name: str
    name_bank: str = "tinkoff"
    initial_amount: float = 10000.0
    interest_rate: float = 20.0
    term_months: int = 6
    date_from: Union[date, None] = None
    capitalization_id: Capitalization = Capitalization.MONTHLY
    deposit_type_id: TypeBankAccount = TypeBankAccount.DEPOSIT


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
    initial_amount: Optional[float] = Field(None, gt=0)
    interest_rate: Optional[float] = Field(None, gt=0)
    term_months: Optional[int] = Field(None, gt=0)
    date_from: Optional[date] = None
    capitalization_id: Optional[Capitalization] = Capitalization.MONTHLY
    deposit_type_id: Optional[TypeBankAccount] = TypeBankAccount.DEPOSIT

    @validator("initial_amount", "interest_rate", "term_months", pre=True)
    def validate_positive_values(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Value must be greater than 0")
        return v
