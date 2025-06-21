
from fastapi import FastAPI
from deposits.router import router as router_deposits

app = FastAPI()
app.include_router(router_deposits)


@app.get("/")
def root():
    return {
        "message": "Savings Portfolio API - Документация доступна по /docs"
    }