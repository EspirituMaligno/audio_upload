from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from database.models import Users
from src.services.dao import UserDAO
from src.api.utils import decode_token


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Users:
    token = credentials.credentials
    try:
        payload = decode_token(token)
    except:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    try:
        user_id = payload["user_id"]
        expire = payload["exp"]
    except:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = await UserDAO.find_one_by_filters(id=user_id)

    if not expire:
        raise HTTPException(status_code=401, detail="Token expired")

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=401, detail="User is blocked")

    return user
