from datetime import date
from pydantic import BaseModel, EmailStr


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str
    first_name: str
    last_name: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
