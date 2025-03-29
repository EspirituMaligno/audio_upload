from pydantic import BaseModel


class AuthResponseDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class MessageResponseDTO(BaseModel):
    message: str
    status_code: int
