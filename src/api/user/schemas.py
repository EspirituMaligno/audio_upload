from datetime import date
from pydantic import BaseModel


class UserUpdateSchema(BaseModel):
    name: str | None = None
    surname: str | None = None
    email: str | None = None
    phone: str | None = None
    date_of_birth: date | None = None
