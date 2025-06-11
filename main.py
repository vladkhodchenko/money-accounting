
from fastapi import FastAPI
from fastapi import HTTPException, status

from models import portfolio_service, Deposit
from schemas import DepositCreate, DepositResponse

from datetime import date


app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "Savings Portfolio API - Документация доступна по /docs"
    }


@app.post("/deposits")
def create_deposit(deposit_data: DepositCreate):
    try:
        existing = portfolio_service.get_deposit_by_name(deposit_data.name)

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Вклад с именем '{deposit_data.name}' уже существует")

        date_from = ""

        if deposit_data.date_from is None:
            date_from = date.today()
        else:
            date_from = deposit_data.date_from

        deposit = Deposit(
            name=deposit_data.name,
            initial_amount=deposit_data.initial_amount,
            interest_rate=deposit_data.interest_rate,
            term_months=deposit_data.term_months,
            date_from=date_from,
            capitalization=deposit_data.capitalization

        )

        portfolio_service.add_deposit(deposit)

        return DepositResponse(
            **deposit_data.dict(),
            date_to=deposit.date_to,
            profit=deposit.calculate_profit(deposit.term_months),
            total_amount=deposit.calculate_amount(deposit.term_months),
        )

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )


@app.get("/deposits")
def get_deposits():
    deposits = portfolio_service.get_deposit_names()
    print(deposits)

    return deposits


@app.patch("deposits/{name}")
@app.get("/deposits/{name}")
def get_deposit(name: str):
    deposit = portfolio_service.get_deposit_by_name(name)

    if not deposit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Вклад с именем '{name}' не найден"
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
