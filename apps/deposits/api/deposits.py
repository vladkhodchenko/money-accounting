import uuid
from datetime import date
from http import HTTPStatus

from fastapi import APIRouter, HTTPException, status
from dateutil.relativedelta import relativedelta

from apps.deposits.controllers.deposits import (
    get_deposit,
    get_deposits,
    create_deposit,
    update_deposit,
    delete_deposit
)
from apps.deposits.controllers.service import DepositService
from apps.deposits.schema.deposits import (
    CreateDepositRequestSchema,
    CreateDepositResponseSchema,
    GetDepositsResponseSchema,
    GetDepositResponseSchema,
    UpdateDepositRequestSchema,
    UpdateDepositResponseSchema,
    DepositSchema
)


router = APIRouter(prefix="/deposits", tags=["Deposits"])


@router.get("/{deposit_id}", response_model=GetDepositResponseSchema)
async def get_deposit(deposit_id: uuid.UUID, deposits_repository):
    return await get_deposit(deposit_id, deposits_repository)


@router.get("", response_model=GetDepositsResponseSchema)
async def get_deposits(user_id: uuid.UUID, deposits_repository):
    return DepositService.find_all()


@router.post("", response_model=CreateDepositResponseSchema)
async def create_deposit(deposit_data: CreateDepositRequestSchema):

    if DepositService.find_name(deposit_data.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Deposit with name '{deposit_data.name}' is exist",
        )

    if (
        deposit_data.initial_amount == 0
        or deposit_data.term_months == 0
        or deposit_data.interest_rate == 0
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect input"
        )

    if deposit_data.date_from is None:
        deposit_data.date_from = date.today()

    date_to = deposit_data.date_from + relativedelta(months=deposit_data.term_months)
    # с точки зрения архитектуры верно ли так делать?

    deposit = CreateDepositRequestSchema(
        name=deposit_data.name,
        name_bank=deposit_data.name_bank,
        deposit_type_id=deposit_data.deposit_type_id,
        initial_amount=deposit_data.initial_amount,
        interest_rate=deposit_data.interest_rate,
        term_months=deposit_data.term_months,
        date_from=deposit_data.date_from,
        capitalization_id=deposit_data.capitalization_id,
    )

    deposit_response = CreateDepositResponseSchema(
        deposit=DepositSchema(
            **deposit_data.model_dump(),
            final_amount=deposit.calculate_amount(deposit.term_months),
            earned_amount=deposit.calculate_profit(deposit.term_months),
            date_to=date_to,
        )
    )

    try:
        DepositService.insert(**deposit_response.model_dump())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error in inserting db"
        )
    return deposit_response


@router.patch("/{name}", response_model=UpdateDepositResponseSchema)
async def update_deposit(deposit_data: UpdateDepositRequestSchema):
    stored_deposit_data = DepositService.find_name(deposit_data.name)

    if stored_deposit_data:
        update_data = deposit_data.model_dump(exclude_unset=True)
        try:
            print(DepositService.update(model_name=deposit_data.name, **update_data))
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error in updating db"
            )
        for key, value in update_data.items():
            setattr(stored_deposit_data, key, value)
        return stored_deposit_data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deposit with name '{deposit_data.name}' not found",
        )


@router.delete("/{name}", status_code=202)
async def delete_deposit(name: str):
    item = DepositService.find_name(name)

    if item:
        DepositService.delete(item)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deposit with name '{name}' not found",
        )
    return HTTPStatus.ACCEPTED
