from datetime import datetime
import os
import uuid
from fastapi import APIRouter, Depends, File, UploadFile, Form
from typing import Annotated

from config import ALLOWED_AUDIO_EXTENSIONS, AUDIO_DIR
from src.services.dao import AudioDAO
from src.api.audio.dto import AudioResponseDTO, MessageResponseDTO
from src.api.audio.schemas import AudioUploadSchema
from src.api.dependecies import get_current_user
from src.database.models import AudioFiles, Users


router = APIRouter(prefix="/audio", tags=["Audio"])


@router.get(
    "/",
    summary="Получение всех аудио файлов пользователя",
    response_model=list[AudioResponseDTO],
)
async def get_all_audio_files(user: Users = Depends(get_current_user)):
    audio_files = await AudioDAO.find_all(user_id=user.id)
    return audio_files


@router.post(
    "/upload", summary="Загрузка аудио файла", response_model=MessageResponseDTO
)
async def upload_audio(
    file: UploadFile = File(...),
    title: Annotated[str, Form()] = None,
    user: Users = Depends(get_current_user),
):
    if not file.content_type.startswith("audio/"):
        return MessageResponseDTO(message="File must be audio format", status_code=400)

    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_AUDIO_EXTENSIONS:
        return MessageResponseDTO(
            message=f"File extension not allowed. Allowed extensions: {', '.join(ALLOWED_AUDIO_EXTENSIONS)}",
            status_code=400,
        )

    os.makedirs("static/audio", exist_ok=True)

    file_name = f"{uuid.uuid4()}{file_extension}"
    file_path = f"static/audio/{file_name}"

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    audio = AudioFiles(
        file_path=str(AUDIO_DIR) + file_path,
        file_name=title or file.filename,
        user_id=user.id,
    )
    await AudioDAO.add_one(audio)

    return MessageResponseDTO(
        message="Audio file uploaded successfully", status_code=200
    )


@router.delete("/", summary="Удаление аудио файла по id")
async def delete_audio(audio_id: int, user: Users = Depends(get_current_user)):
    await AudioDAO.delete_one(id=audio_id, user_id=user.id)
    return MessageResponseDTO(
        message="Audio file deleted successfully", status_code=200
    )
