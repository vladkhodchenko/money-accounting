
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from deposits.router import router as router_deposits

app = FastAPI()
app.include_router(router_deposits)


origins = [
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Savings Portfolio API - Документация доступна по /docs"
    }