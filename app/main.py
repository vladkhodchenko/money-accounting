
from fastapi import FastAPI
from fastapi import HTTPException, status
from datetime import date

from logic import Deposit
from deposits.schemas import SDepositCreate, SDepositResponse
from deposits.router import router as router_deposits

app = FastAPI()
app.include_router(router_deposits)


@app.get("/")
def root():
    return {
        "message": "Savings Portfolio API - Документация доступна по /docs"
    }