import time

from jose import ExpiredSignatureError
import pytest
from src.api.utils import (
    hash_password,
    check_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)


def test_hashing_password():
    password = "password123"
    hashed_password = hash_password(password)
    assert check_password(password, hashed_password)
    assert not check_password("wrong_password", hashed_password)


def test_token_creation_and_decoding():
    data = {"sub": "audio_upload", "user_id": 1}
    token = create_access_token(data)
    refresh_token = create_refresh_token(data)

    assert refresh_token is not None
    assert isinstance(refresh_token, str)

    assert token is not None
    assert isinstance(token, str)

    payload = decode_token(token)
    assert payload["sub"] == "audio_upload"
    assert payload["user_id"] == 1
    assert "exp" in payload
    assert payload["type"] == "access"


def test_expired_token():
    data = {"sub": "audio_upload", "user_id": 1}
    token = create_access_token(data)

    time.sleep(3)

    with pytest.raises(ExpiredSignatureError):
        decode_token(token)
