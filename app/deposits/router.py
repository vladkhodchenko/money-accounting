from fastapi import APIRouter
from database import session
from deposits.service import DepositService

router = APIRouter(
    prefix = "/deposits",
    tags = ["Deposits"]
)

@router.get("")
def get_deposits():
    result = DepositService.find_all()
    return result


@router.get("/{deposit_id}")
def get_deposit(deposit_id):
    return DepositService.find_by_id(deposit_id)


@router.patch("/{deposit_id}")
def patch_deposit(deposit_id):
    pass