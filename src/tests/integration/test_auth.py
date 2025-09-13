from http import HTTPStatus
from unittest.mock import AsyncMock, patch
import pytest

from src.api.auth.router import signup, login
from src.api.auth.dto import MessageResponseDTO
from src.api.auth.schemas import UserCreateSchema, UserLoginSchema, AuthResponseDTO
from fastapi import Request


@pytest.mark.asyncio
async def test_signup_success():
    data = UserCreateSchema(
        email="test@example.com",
        password="password123",
        confirm_password="password123",
        first_name="Test",
        last_name="User",
    )

    fake_request = AsyncMock()
    fake_request.client.host = "8.8.8.8"

    with patch(
        "src.api.auth.router.UserDAO.find_one_by_filters", new_callable=AsyncMock
    ) as mock_find:
        with patch(
            "src.api.auth.router.UserDAO.add_one", new_callable=AsyncMock
        ) as mock_add:
            with patch(
                "src.api.auth.router.get_timezone_by_ip", return_value="Europe/Moscow"
            ):

                mock_find.return_value = None

                response = await signup(data, fake_request)

                assert isinstance(response, MessageResponseDTO)
                assert response.status_code == HTTPStatus.CREATED
                assert response.message == "Пользователь успешно зарегистрирован"
                mock_add.assert_awaited_once()


@pytest.mark.asnycio
async def test_login_endpoint():
    data = UserLoginSchema(email="test@example.com", password="password123")

    with patch(
        "src.api.auth.router.UserDAO.find_one_by_filters", new_callable=AsyncMock
    ) as mock_find:
        mock_find.return_value = None

        response = await login(data)

        assert isinstance(response, AuthResponseDTO)
        assert response.status_code == 200
        assert response.message == 