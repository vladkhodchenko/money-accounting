from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from auth.service import UserService
from passlib.context import CryptContext
from auth.schemas import User, UserBase, UserInDB
import secrets
import jwt

router = APIRouter(prefix="/who", tags=["Auth"])

secret_user: str = "user"
secret_password: str = "password"
basic: HTTPBasicCredentials = HTTPBasic()

myctx = CryptContext(schemes=["sha256_crypt", "des_crypt"])

fake_db = [UserInDB(name='user2', hashed_password='$5$rounds=535000$PGFQ/exkYHEEoTrq$YtFhsWSVPyf72bbtpHR3FXioMtQFPoVgbRatfrhifn.')]


@router.post("/register")
def register(register_data: User) -> UserBase:
    pwd = register_data.password
    hashed_password = myctx.hash(register_data.password)
    
    user_in_db = UserInDB(
        name = register_data.name,
        hashed_password = hashed_password,
        # email = register_data.email
    )
    
    fake_db.append(user_in_db)

    user = UserBase(
        name = register_data.name,
        # email = register_data.email
    )
    print(fake_db)
    return user


@router.post("/login")
def login(user_data: User):
    is_exist = is_exist_user(fake_db, user_data.name)
    if is_exist:
        if myctx.verify(user_data.password, is_exist.hashed_password):
            print("sucess")
        else:
            raise HTTPException(
            status_code=401, detail="Incorrect password"
        )
    else:
        raise HTTPException(
            status_code=401, detail="Incorrect username or password"
        )
    
def is_exist_user(db, name):
    for user in db:
        if user.name == name:
            return user
        return False


# Basic auth
@router.get("")
def get_user(creds: HTTPBasicCredentials = Depends(basic)) -> dict:
    if creds.username == secret_user and creds.password == secret_password:
        return {"username": creds.username, "password": creds.password}
    raise HTTPException(
        status_code=401,
        headers={"WWW-Authenticate": "Basic"},
        detail="Hey!"
    )


@router.get("/logout")
def logout():
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You have successfully logged out",
            headers={"WWW-Authenticate": "Basic"},
        )