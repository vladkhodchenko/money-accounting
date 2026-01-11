from pydantic import BaseModel, Field, validator


class UserBase(BaseModel):
    name: str
    # email: str


class User(UserBase):
    password: str


class UserInDB(UserBase):
    hashed_password: str
    # email: str
