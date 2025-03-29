from datetime import datetime
from fastapi import APIRouter, HTTPException, status

from fastapi.responses import JSONResponse, RedirectResponse

from config import API_REDIRECT_URL, YANDEX_CLIENT_ID, YANDEX_CLIENT_SECRET

from database.models import Users
from src.database.db import async_session


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get(
    "/yandex/redirect", summary="Роут дергается по нажатию кнопки войти через яндекс"
)
async def yandex_redirect():
    return RedirectResponse(
        f"https://oauth.yandex.ru/authorize?response_type=code&client_id={YANDEX_CLIENT_ID}&redirect_uri={YANDEX_REDIRECT_URI}"
    )


@router.get("/yandex/callback", summary="Роут вызывается сам")
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

        user = await get_user_by_number(user_num)

        if not user:
            async with async_session() as session:
                user = Users(
                    number=user_num,
                    created_at=datetime.now(),
                    time_zone=time_zone_user,
                )
                session.add(user)
                await session.commit()

        user.time_zone = time_zone_user
        async with async_session() as session:
            session.add(user)
            await session.commit()

        token = create_access_token(data={"sub": "audio_upload", "user_id": user.id})

        refresh_token = create_refresh_token(
            data={"sub": "audio_upload", "user_id": user.id}
        )

        return RedirectResponse(
            f"prosvet://auth?token={token}&refresh={refresh_token}&allData={all_data}"
        )
