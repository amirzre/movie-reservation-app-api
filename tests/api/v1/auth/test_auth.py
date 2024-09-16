import pytest
from fastapi import status
from httpx import AsyncClient

from app.schemas.request import UserLoginRequest


@pytest.mark.asyncio
class TestAuthEndpoints:
    async def test_login_success(self, client: AsyncClient, register_normal_user: dict):
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": register_normal_user.get("email"), "password": register_normal_user.get("password")},
        )
        assert response.status_code == status.HTTP_200_OK
        assert "Access-Token" in response.cookies
        assert "Refresh-Token" in response.cookies

    async def test_login_failure(self, client: AsyncClient):
        login_request = UserLoginRequest(email="user@example.com", password="wrongpassword")
        response = await client.post("/api/v1/auth/login", json=login_request.model_dump())
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_refresh_success(self, client: AsyncClient, auth_token_user: tuple[str, str]):
        _, refresh_token = auth_token_user
        response = await client.post("/api/v1/auth/refresh", cookies={"Refresh-Token": refresh_token})
        assert response.status_code == status.HTTP_200_OK
        assert "Access-Token" in response.cookies
        assert "Refresh-Token" in response.cookies

    async def test_refresh_failure(self, client: AsyncClient):
        response = await client.post("/api/v1/auth/refresh", cookies={"Refresh-Token": "invalidtoken"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_me_success(self, client: AsyncClient, auth_token_user: tuple[str, str]):
        access_token, _ = auth_token_user
        response = await client.get("/api/v1/auth/me", cookies={"Access-Token": access_token})
        assert response.status_code == status.HTTP_200_OK
        user_data = response.json()
        assert "email" in user_data

    async def test_me_unauthorized(self, client: AsyncClient):
        response = await client.get("/api/v1/auth/me")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_logout_success(self, client: AsyncClient, auth_token_user: tuple[str, str]):
        access_token, refresh_token = auth_token_user
        response = await client.delete(
            "/api/v1/auth/logout", cookies={"Access-Token": access_token, "Refresh-Token": refresh_token}
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert "Access-Token" not in response.cookies
        assert "Refresh-Token" not in response.cookies

    async def test_logout_unauthorized(self, client: AsyncClient):
        response = await client.delete("/api/v1/auth/logout")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
