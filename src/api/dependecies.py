from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from src.database.models import Users
from src.services.dao import UserDAO
from src.api.utils import decode_token

security = HTTPBearer()


async def get_user_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Users:
    token = credentials.credentials
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload["user_id"]
    except (JWTError, KeyError):
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await UserDAO.find_one_by_filters(id=user_id)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is blocked")

    return user


async def get_current_user(
    user: Users = Depends(get_user_from_token),
) -> Users:
    return user


async def get_current_admin(
    user: Users = Depends(get_user_from_token),
) -> Users:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="You are not an admin")

    return user
