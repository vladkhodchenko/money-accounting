from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from auth.service import 

router = APIRouter(prefix="/who", tags=["Auth"])

secret_user: str = "user"
secret_password: str = "password"
basic: HTTPBasicCredentials = HTTPBasic()


@router.get("")
def get_user(creds: HTTPBasicCredentials = Depends(basic)) -> dict:
    if creds.username == secret_user and creds.password == secret_password:
        return {"username": creds.username, "password": creds.password}
    raise HTTPException(status_code=401, detail="Hey!")


@router.post("")
def post_user(user_data):
    pass


@router.post("")
def create_session(user_data):
    pass