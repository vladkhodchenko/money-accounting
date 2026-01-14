from pydantic import BaseModel, Field, UUID4
from datetime import date
from services.database.models.deposits import Capitalization, TypeBankAccount


class DepositSchema(BaseModel):
    id: UUID4
    user_id: UUID4

    name: str
    name_bank: str

    initial_amount: float
    final_amount: float
    earned_amount: float

    interest_rate: float
    term_months: int

    date_from: date | None
    date_to: date

    capitalization_id: Capitalization = Capitalization.MONTHLY
    deposit_type_id: TypeBankAccount = TypeBankAccount.DEPOSIT
    created_at: date
    updated_at: date


class CreateDepositRequestSchema(BaseModel):
    name: str
    name_bank: str = "tinkoff"
    user_id: UUID4

    initial_amount: float = 10000.0
    interest_rate: float = 20.0
    term_months: int = 6

    date_from: date | None = None

    capitalization_id: Capitalization = Capitalization.MONTHLY
    deposit_type_id: TypeBankAccount = TypeBankAccount.DEPOSIT


class CreateDepositResponseSchema(BaseModel):
    deposit: DepositSchema


class GetDepositResponseSchema(BaseModel):
    deposit: DepositSchema


class GetDepositsQuerySchema(BaseModel):
    user_id: str


class GetDepositsResponseSchema(BaseModel):
    deposits: list[DepositSchema]


class UpdateDepositRequestSchema(BaseModel):
    name: str | None = None
    name_bank: str | None = None
    initial_amount: float | None = Field(None, gt=0)
    interest_rate: float | None = Field(None, gt=0)
    term_months: int | None = Field(None, gt=0)
    date_from: date | None = None
    capitalization_id: Capitalization = Capitalization.MONTHLY
    deposit_type_id: TypeBankAccount = TypeBankAccount.DEPOSIT


class UpdateDepositResponseSchema(BaseModel):
    deposit: DepositSchema
