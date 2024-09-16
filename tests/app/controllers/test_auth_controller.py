from unittest.mock import AsyncMock, MagicMock

import pytest
from redis.asyncio import client

from app.controllers import AuthController
from app.models import User
from app.repositories import UserRepository
from core.exceptions import BadRequestException, NotFoundException
from core.security import JWTHandler, PasswordHandler


@pytest.mark.asyncio
class TestAuthController:
    @pytest.fixture
    def user_repository(self):
        return AsyncMock(spec=UserRepository)

    @pytest.fixture
    def cache(self):
        return AsyncMock(spec=client.Redis)

    @pytest.fixture
    def auth_controller(self, user_repository):
        return AuthController(user_repository=user_repository)

    @pytest.fixture
    def user(self):
        return User(uuid="user-uuid", email="test@example.com", password="hashed_password", role="user", activated=True)

    async def test_login_success(self, auth_controller, user_repository, cache, user):
        user_repository.get_by_email.return_value = user
        PasswordHandler.verify = MagicMock(return_value=True)
        JWTHandler.encode = MagicMock(return_value="access_token")
        JWTHandler.encode_refresh_token = MagicMock(return_value="refresh_token")

        cache.set = AsyncMock(return_value=None)

        token = await auth_controller.login(email=user.email, password="password", cache=cache)

        assert token.access_token == "access_token"
        assert token.refresh_token == "refresh_token"
        cache.set.assert_called_once()

    async def test_login_invalid_credentials(self, auth_controller, user_repository):
        user_repository.get_by_email.return_value = None

        with pytest.raises(BadRequestException):
            await auth_controller.login(email="wrong@example.com", password="password", cache=AsyncMock())

    async def test_login_incorrect_password(self, auth_controller, user_repository, user):
        user_repository.get_by_email.return_value = user
        PasswordHandler.verify = MagicMock(return_value=False)

        with pytest.raises(BadRequestException):
            await auth_controller.login(email=user.email, password="wrong_password", cache=AsyncMock())

    async def test_login_inactive_user(self, auth_controller, user_repository, user):
        user.activated = False
        user_repository.get_by_email.return_value = user
        PasswordHandler.verify = MagicMock(return_value=True)

        with pytest.raises(BadRequestException):
            await auth_controller.login(email=user.email, password="password", cache=AsyncMock())

    async def test_refresh_success(self, auth_controller, user_repository, cache, user):
        user_repository.get_by_uuid.return_value = user
        cache.get = AsyncMock(return_value=user.uuid)
        cache.ttl = AsyncMock(return_value=300)

        JWTHandler.encode = MagicMock(return_value="new_access_token")
        JWTHandler.encode_refresh_token = MagicMock(return_value="new_refresh_token")

        cache.set = AsyncMock(return_value=None)
        cache.delete = AsyncMock(return_value=None)

        token = await auth_controller.refresh(old_refresh_token="old_refresh_token", cache=cache)

        assert token.access_token == "new_access_token"
        assert token.refresh_token == "new_refresh_token"
        cache.set.assert_called_once()
        cache.delete.assert_called_once()

    async def test_logout_success(self, auth_controller, cache):
        cache.delete = AsyncMock(return_value=1)

        await auth_controller.logout(refresh_token="valid_refresh_token", cache=cache)

        cache.delete.assert_called_once_with("valid_refresh_token")

    async def test_logout_token_not_found(self, auth_controller, cache):
        with pytest.raises(NotFoundException):
            await auth_controller.logout(refresh_token=None, cache=cache)
