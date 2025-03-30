from pydantic import BaseModel


class AudioUploadSchema(BaseModel):
    title: str | None = None
