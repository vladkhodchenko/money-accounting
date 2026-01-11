from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer

from passlib.context import CryptContext
from apps.auth.schemas import User, UserBase, UserInDB
import jwt
import apps.auth.security

router = APIRouter(prefix="/who", tags=["Auth"])

secret_user: str = "user"
secret_password: str = "password"
basic: HTTPBasicCredentials = HTTPBasic()

myctx = CryptContext(schemes=["sha256_crypt", "des_crypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


fake_db = [
    UserInDB(
        name="user2",
        hashed_password="$5$rounds=535000$fzF/wlaG/XuHFr2p$gvAFxA2n1CDRqkW6JmjWDELVEElRRBgViHi1H48qK7C",
    )
]  # password = "password"


@router.post("/register")
def register(register_data: User) -> UserBase:
    pwd = register_data.password
    hashed_password = myctx.hash(register_data.password)
    user_in_db = UserInDB(
        name=register_data.name,
        hashed_password=hashed_password,
        # email = register_data.email
    )

    fake_db.append(user_in_db)

    user = UserBase(
        name=register_data.name,
        # email = register_data.email
    )
    print(fake_db)
    return user


@router.post("/login")
def login(user_data: User):
    print(fake_db)
    is_exist = is_exist_user(fake_db, user_data.name)
    if is_exist:
        if myctx.verify(user_data.password, is_exist.hashed_password):
            print("sucess")
        else:
            raise HTTPException(status_code=401, detail="Incorrect password")
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password")


def is_exist_user(db, name):
    for user in db:
        print(user)
        if user.name == name:
            return user
        return None


# Basic auth
@router.get("")
def get_user(creds: HTTPBasicCredentials = Depends(basic)) -> dict:
    if creds.username == secret_user and creds.password == secret_password:
        return {"username": creds.username, "password": creds.password}
    raise HTTPException(
        status_code=401, headers={"WWW-Authenticate": "Basic"}, detail="Hey!"
    )


@router.get("/logout")
def logout():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You have successfully logged out",
        headers={"WWW-Authenticate": "Basic"},
    )


@router.post("/login_jwt")
def login_jwt(user_data: User):
    is_exist = is_exist_user(fake_db, user_data.name)
    print(is_exist)
    if is_exist:
        if myctx.verify(user_data.password, is_exist.hashed_password):
            token = apps.auth.security.create_jwt_token({"sub": user_data.name})
            return {"token": token}
        else:
            raise HTTPException(status_code=401, detail="Incorrect password")
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password")


@router.get("/protected_resource")
def protect_resource(token: str = Depends(oauth2_scheme)):
    # user = is_exist_user(fake_db, current_user)
    print(token)
    # try:
    #     payload = jwt.decode(token, auth.security.SECRET_KEY, algorithms=[auth.security.ALGORITHM])
    #     print(payload)
    # except jwt.ExpiredSignatureError:
    #     raise HTTPException(status_code=401, detail="Token has expired", headers={"WWW-Authenticate": "Bearer"})
    # except jwt.DecodeError:
    #     raise HTTPException(status_code=401, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})
    # return user
