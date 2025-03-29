import os
from dotenv import load_dotenv

load_dotenv()


# DATABASE
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

POSTGRES_URL = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB,
)


# YANDEX OAUTH API
YANDEX_CLIENT_SECRET = os.getenv("YANDEX_CLIENT_SECRET")
YANDEX_CLIENT_ID = os.getenv("YANDEX_CLIENT_ID")
YANDEX_REDIRECT_URI = "https://vlad.ayarayrovich.ru/api/v1/auth/yandex/callback"
API_REDIRECT_URL = "https://vlad.ayarayrovich.ru/docs"
