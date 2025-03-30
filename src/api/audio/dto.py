from datetime import datetime
from pydantic import BaseModel


class MessageResponseDTO(BaseModel):
    message: str
    status_code: int


class AudioResponseDTO(BaseModel):
    id: int
    file_name: str
    file_path: str
    created_at: datetime
