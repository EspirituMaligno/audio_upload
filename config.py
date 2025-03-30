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


# JWT
PUBLIC_KEY = str(os.getenv("PUBLIC_KEY"))

ALGORITHM = "HS256"


# YANDEX OAUTH API
YANDEX_CLIENT_SECRET = os.getenv("YANDEX_CLIENT_SECRET")
YANDEX_CLIENT_ID = os.getenv("YANDEX_CLIENT_ID")
YANDEX_REDIRECT_URI = "https://vlad.ayarayarovich.ru/api/v1/auth/yandex/callback"
API_REDIRECT_URL = "https://vlad.ayarayarovich.ru/docs"


# AUDIO
AUDIO_DIR = "localhost:5000/"
ALLOWED_AUDIO_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".ogg",
    ".m4a",
    ".flac",
    ".aac",
    ".wma",
    ".aiff",
}
