from datetime import timedelta, date
from fastapi import APIRouter, HTTPException, status
from dateutil.relativedelta import relativedelta

from consts import Capitalization
from database import session
from deposits.service import DepositService
from deposits.schemas import SDepositCreate, SDepositResponse
from logic import Deposit



router = APIRouter(
    prefix = "/deposits",
    tags = ["Deposits"]
)


@router.get("")
def get_deposits():
    return DepositService.find_all()


@router.get("/{deposit_id}")
def get_deposit(deposit_id) -> SDepositResponse:
    return DepositService.find_by_id(deposit_id)


@router.get("/{name}")
def get_deposit(name: str):
    deposit = portfolio_service.get_deposit_by_name(name)

    if not deposit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deposit with name '{name}' not found"
        )

    return DepositResponse(
        name=deposit.name,
        initial_amount=deposit.initial_amount,
        interest_rate=deposit.interest_rate,
        term_months=deposit.term_months,
        date_from=deposit.date_from,
        capitalization=deposit.capitalization,
        date_to=deposit.date_to,
        profit=deposit.calculate_profit(deposit.term_months),
        total_amount=deposit.calculate_amount(deposit.term_months)
)


# @router.patch("/{deposit_id}")
# def patch_deposit(deposit_id) -> SDepositCreate:
#     return DepositService.find_by_id(deposit_id)


@router.post("")
def create_deposit(deposit_data: SDepositCreate) -> SDepositResponse:
    existing = DepositService.find_name(deposit_data.name)
    if existing:
          raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Вклад с именем '{deposit_data.name}' уже существует")

    if deposit_data.date_from is None:
        deposit_data.date_from = date.today()

    
    date_to = deposit_data.date_from + relativedelta(months=deposit_data.term_months)

    deposit = Deposit(
        name=deposit_data.name,
        name_bank = deposit_data.name_bank,
        # type_account = deposit_data.type_account,
        initial_amount=deposit_data.initial_amount,
        interest_rate=deposit_data.interest_rate,
        term_months=deposit_data.term_months,
        date_from=deposit_data.date_from,
        capitalization_id=deposit_data.capitalization_id,
    )
    
    deposit_response = SDepositResponse(
        **deposit_data.dict(),
        final_amount = deposit.calculate_amount(deposit.term_months),
        earned_amount = deposit.calculate_profit(deposit.term_months),
        date_to = date_to,
    )
    
    # try:
    DepositService.insert(**deposit_response.dict())
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST
    #     )

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


