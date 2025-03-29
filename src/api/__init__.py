from fastapi import APIRouter
from src.api.auth.router import router as auth_router
from src.api.user.router import router as user_router
from src.api.audio.router import router as audio_router

main_router = APIRouter()


main_router.include_router(auth_router)
main_router.include_router(user_router)
main_router.include_router(audio_router)

__all__ = ["main_router"]
