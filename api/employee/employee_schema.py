from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional


class emoloyee_schemas(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone: int
    Role: str
    Date_of_birth: date

    class Config:
        orm_mode = True


class emoloyee_schemas_update(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: int
    Role: str
    Date_of_birth: date


class modify_emoloyee_schemas_update(BaseModel):
    first_name: str = None
    last_name: str = None
    email: str = None
    phone: int = None
    Role: str = None
    Date_of_birth: date = None


class Settings(BaseModel):
    authjwt_secret_key: str = (
        "d5f4db479ec02bbf0b6f41616bbc2d7f895a3774a02cd9505352647cc27c3cc5"
    )


class LoginModel(BaseModel):
    email: str
    password: str
