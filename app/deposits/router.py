from datetime import date
from fastapi import APIRouter, HTTPException, status
from dateutil.relativedelta import relativedelta

from consts import Capitalization
from database import session
from deposits.service import DepositService
from deposits.schemas import SDepositCreate, SDeposit, SDepositPatch
from logic import Deposit


router = APIRouter(
    prefix="/deposits",
    tags=["Deposits"]
)


@router.get("")
def get_deposits():
    return DepositService.find_all()


@router.get("/{deposit_id}")
def get_deposit_by_id(deposit_id: int):
    return DepositService.find_by_id(deposit_id)


@router.get("/{name}")
def get_deposit_by_name(name: str):
    return DepositService.find_name(name)
    deposit = DepositService.find_name(name)
    print(deposit)
    if not deposit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deposit with name '{name}' not found"
        )

    return deposit


@router.patch("/{name}")
def patch_deposit(deposit_data: SDepositPatch)-> SDeposit:
    stored_deposit_data = DepositService.find_name(deposit_data.name)
    if stored_deposit_data:
        update_data = deposit_data.dict(exclude_unset=True)
        try:
            result = DepositService.update(model_name=deposit_data.name, **update_data)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error in updating db"
            )
        for key, value in update_data.items():
            setattr(stored_deposit_data, key, value)
        return stored_deposit_data
    else: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deposit with name '{deposit_data.name}' not found"
        )
    
   
@router.post("")
def create_deposit(deposit_data: SDepositCreate) -> SDeposit:
    if DepositService.find_name(deposit_data.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Deposit with name '{deposit_data.name}' is exist"
        )

    if deposit_data.initial_amount == 0 or \
            deposit_data.term_months == 0 or \
            deposit_data.interest_rate == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect input"
        )

    if deposit_data.date_from is None:
        deposit_data.date_from = date.today()

    date_to = deposit_data.date_from + \
        relativedelta(months=deposit_data.term_months)

    deposit = Deposit(
        name=deposit_data.name,
        name_bank=deposit_data.name_bank,
        # type_account = deposit_data.type_account,
        initial_amount=deposit_data.initial_amount,
        interest_rate=deposit_data.interest_rate,
        term_months=deposit_data.term_months,
        date_from=deposit_data.date_from,
        capitalization_id=deposit_data.capitalization_id,
    )

    deposit_response = SDeposit(
        **deposit_data.dict(),
        final_amount=deposit.calculate_amount(deposit.term_months),
        earned_amount=deposit.calculate_profit(deposit.term_months),
        date_to=date_to,
    )

    try:
        DepositService.insert(**deposit_response.dict())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error in inserting db"
        )
    return deposit_response


@router.delete("/{name}")
def delete_deposit(name: str):
    item = DepositService.find_name(name)
    if item:
        DepositService.delete(item)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deposit with name '{name}' not found"
        )
