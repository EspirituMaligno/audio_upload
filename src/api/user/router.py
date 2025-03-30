from fastapi import APIRouter, Depends, Query

from src.api.auth.dto import MessageResponseDTO
from src.api.user.schemas import UserUpdateSchema
from src.services.dao import UserDAO
from src.api.dependecies import get_current_admin, get_current_user
from src.api.user.dto import UserResponseDTO
from src.database.models import Users


router = APIRouter(prefix="/user", tags=["User"])


@router.get(
    "/", summary="Получение информации о пользователе", response_model=UserResponseDTO
)
async def get_me(user: Users = Depends(get_current_user)):
    return user


@router.put(
    "/", summary="Обновление информации о пользователе", response_model=UserResponseDTO
)
async def update_user(data: UserUpdateSchema, user: Users = Depends(get_current_user)):
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}

    if not update_data:
        return user

    user_updated = await UserDAO.update_one(user.id, **update_data)
    return user_updated


@router.delete("/", summary="Удаление пользователя", response_model=MessageResponseDTO)
async def delete_user(
    user_id: int = Query(..., description="ID пользователя"),
    admin: Users = Depends(get_current_admin),
):
    await UserDAO.delete_one(id=user_id)

    return MessageResponseDTO(message="User deleted successfully", status_code=200)
