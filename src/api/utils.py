import requests
from fastapi.responses import JSONResponse
from jose import jwt
from datetime import date, datetime, timedelta, timezone

from config import ALGORITHM, PUBLIC_KEY


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, PUBLIC_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, PUBLIC_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token, PUBLIC_KEY, algorithms=[ALGORITHM], options={"verify_exp": True}
        )
        token_type = payload.get("type")

        if token_type not in ["access", "refresh"]:
            return JSONResponse({"status": "Invalid type token"}, 401)

        if "exp" in payload:
            expire = datetime.fromtimestamp(payload["exp"], timezone.utc)
            if expire < datetime.now(timezone.utc):
                return JSONResponse({"status": "Token expired"}, 401)

        return payload
    except jwt.JWTError as e:
        print(f"JWTError: {e}")
        return JSONResponse({"status": "Invalid credentials"}, 401)


def get_timezone_by_ip(ip_address):
    response = requests.get(f"https://ipinfo.io/{ip_address}/json")
    data = response.json()
    return data.get("timezone")
