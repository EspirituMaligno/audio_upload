from src.database.models import AudioFiles, Users
from src.services.base import BaseDAO


class UserDAO(BaseDAO):
    model = Users


class AudioDAO(BaseDAO):
    model = AudioFiles
