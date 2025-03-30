from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request, status

from fastapi import security
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.api.auth.schemas import UserCreateSchema, UserLoginSchema
from src.api.auth.dto import AuthResponseDTO, MessageResponseDTO
from src.api.utils import (
    check_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_timezone_by_ip,
    hash_password,
)
from config import (
    API_REDIRECT_URL,
    YANDEX_CLIENT_ID,
    YANDEX_CLIENT_SECRET,
    YANDEX_REDIRECT_URI,
)

from src.database.models import Users
from src.services.dao import UserDAO
from src.database.db import async_session

from httpx import AsyncClient


router = APIRouter(prefix="/auth", tags=["Auth"])


security = HTTPBearer()


@router.get(
    "/yandex/redirect", summary="Роут дергается по нажатию кнопки войти через яндекс"
)
async def yandex_redirect():
    return f"https://oauth.yandex.ru/authorize?response_type=code&client_id={YANDEX_CLIENT_ID}&redirect_uri={YANDEX_REDIRECT_URI}"
    return RedirectResponse(
        f"https://oauth.yandex.ru/authorize?response_type=code&client_id={YANDEX_CLIENT_ID}&redirect_uri={YANDEX_REDIRECT_URI}"
    )


@router.get(
    "/yandex/callback", summary="Роут вызывается сам", response_model=AuthResponseDTO
)
async def yandex_callback(code: str, request: Request):
    ip_address = request.client.host
    time_zone_user = get_timezone_by_ip(ip_address)
    async with AsyncClient() as client:
        response = await client.post(
            "https://oauth.yandex.ru/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": YANDEX_CLIENT_ID,
                "client_secret": YANDEX_CLIENT_SECRET,
                "redirect_uri": API_REDIRECT_URL,
            },
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не удалось получить токен",
            )
        token_data = response.json()
        access_token = token_data["access_token"]

        userinfo_response = await client.get(
            "https://login.yandex.ru/info",
            headers={"Authorization": f"OAuth {access_token}"},
        )
        if userinfo_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не удалось получить информацию о пользователе",
            )
        userinfo = userinfo_response.json()
        num_not_clear = userinfo["default_phone"]["number"]
        if not num_not_clear:
            return JSONResponse({"message": "Provide access to the number"}, 401)
        user_num = num_not_clear.replace("+", "")

        user = await UserDAO.find_one_by_filters(phone=user_num)

        birthday = datetime.strptime(userinfo["birthday"], "%Y-%m-%d")

        if not user:
            user = Users(
                name=userinfo["first_name"],
                surname=userinfo["last_name"],
                email=userinfo["default_email"],
                date_of_birth=birthday,
                phone=user_num,
                time_zone=time_zone_user,
            )
            await UserDAO.add_one(user)

        await UserDAO.update_one(user.id, time_zone=time_zone_user)

        token = create_access_token(data={"sub": "audio_upload", "user_id": user.id})

        refresh_token = create_refresh_token(
            data={"sub": "audio_upload", "user_id": user.id}
        )

        return AuthResponseDTO(
            access_token=token, refresh_token=refresh_token, token_type="Bearer"
        )


@router.post("/refresh", summary="Обновление токена", response_model=AuthResponseDTO)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = decode_token(token)
        user_id = payload["user_id"]
        type = payload["type"]
    except Exception as e:
        print(e)
        return MessageResponseDTO(
            message="Invalid token", status_code=status.HTTP_401_UNAUTHORIZED
        )

    user = await UserDAO.find_one_by_filters(id=user_id)

    if type != "refresh":
        return MessageResponseDTO(
            message="You token is not refresh", status_code=status.HTTP_401_UNAUTHORIZED
        )

    if not user:
        return MessageResponseDTO(
            message="User not authorized", status_code=status.HTTP_404_NOT_FOUND
        )

    token = create_access_token(data={"sub": "audio_upload", "user_id": user.id})

    refresh_token = create_refresh_token(
        data={"sub": "audio_upload", "user_id": user.id}
    )

    return AuthResponseDTO(
        access_token=token, refresh_token=refresh_token, token_type="Bearer"
    )


@router.post(
    "/signup", summary="Регистрация пользователя", response_model=MessageResponseDTO
)
async def signup(data: UserCreateSchema, request: Request):
    ip_address = request.client.host
    time_zone_user = get_timezone_by_ip(ip_address)
    if data.password != data.confirm_password:
        return MessageResponseDTO(
            message="Пароли не совпадают",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    user = await UserDAO.find_one_by_filters(email=data.email)
    if user:
        return MessageResponseDTO(
            message="Пользователь с таким email уже существует",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    user = Users(
        email=data.email,
        hash_password=hash_password(data.password),
        name=data.first_name,
        surname=data.last_name,
        time_zone=time_zone_user,
    )

    await UserDAO.add_one(user)

    return MessageResponseDTO(
        message="Пользователь успешно зарегистрирован",
        status_code=status.HTTP_201_CREATED,
    )


@router.post("/login", summary="Вход в систему", response_model=AuthResponseDTO)
async def login(data: UserLoginSchema):
    user = await UserDAO.find_one_by_filters(email=data.email)

    if not user:
        return MessageResponseDTO(
            message="User not found", status_code=status.HTTP_401_UNAUTHORIZED
        )

    if not check_password(data.password, user.hash_password):
        return MessageResponseDTO(
            message="Wrong password", status_code=status.HTTP_401_UNAUTHORIZED
        )

    token = create_access_token(data={"sub": "audio_upload", "user_id": user.id})

    refresh_token = create_refresh_token(
        data={"sub": "audio_upload", "user_id": user.id}
    )

    return AuthResponseDTO(
        access_token=token, refresh_token=refresh_token, token_type="Bearer"
    )
