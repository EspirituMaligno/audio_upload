from datetime import date

from pydantic import BaseModel


class UserResponseDTO(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    phone: str
    date_of_birth: date
    role: str


class MessageResponseDTO(BaseModel):
    message: str
    status_code: int
