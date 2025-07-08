from pydantic import BaseModel, Field, validator

class User(BaseModel):
    name: str
    hash_password: str
    email: str

