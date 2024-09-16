from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from app.controllers.user import UserController
from app.models import User
from app.models.user import UserRole
from app.repositories import UserRepository
from core.db.session import reset_session_context, set_session_context
from core.exceptions import BadRequestException, NotFoundException
from core.security import PasswordHandler


@pytest.fixture
def user_repository():
    """Fixture to mock UserRepository."""
    return AsyncMock(spec=UserRepository)


@pytest.fixture
def user_controller(user_repository):
    """Fixture to create an instance of UserController with mocked repository."""
    return UserController(user_repository=user_repository)


@pytest.fixture(autouse=True)
def mock_session_context():
    """Fixture to mock the session context for the tests."""
    token = set_session_context("test-session")
    yield
    reset_session_context(token)


@pytest.fixture(autouse=True)
def mock_db_session():
    """Fixture to mock database session for the tests."""
    with patch("core.db.session.get_session", new_callable=AsyncMock):
        yield


@pytest.mark.asyncio
class TestUserController:
    async def test_get_user_success(self, user_controller, user_repository):
        user_uuid = uuid4()
        mock_user = User(id=1, uuid=user_uuid, email="test@example.com")
        user_repository.get_by_uuid.return_value = mock_user

        result = await user_controller.get_user(user_uuid=user_uuid)

        assert result == mock_user
        user_repository.get_by_uuid.assert_called_once_with(uuid=user_uuid)

    async def test_get_user_not_found(self, user_controller, user_repository):
        user_uuid = uuid4()
        user_repository.get_by_uuid.return_value = None

        with pytest.raises(NotFoundException):
            await user_controller.get_user(user_uuid=user_uuid)

        user_repository.get_by_uuid.assert_called_once_with(uuid=user_uuid)

    async def test_register_success(self, user_controller, user_repository):
        email = "test@example.com"
        password = "password123"
        hashed_password = "hashed_password123"

        user_repository.get_by_email.return_value = None
        mock_user = User(id=1, email=email)
        user_repository.create.return_value = mock_user

        with patch.object(PasswordHandler, "hash", return_value=hashed_password):
            result = await user_controller.register(
                email=email,
                first_name="test",
                last_name="user",
                password=password,
                role=UserRole.USER,
                activated=True,
            )

        assert result == mock_user
        user_repository.get_by_email.assert_called_once_with(email=email)
        user_repository.create.assert_called_once_with(
            {
                "email": email,
                "first_name": "test",
                "last_name": "user",
                "role": UserRole.USER,
                "activated": True,
                "password": hashed_password,
            }
        )

    async def test_register_user_already_exists(self, user_controller, user_repository):
        email = "test@example.com"
        mock_user = User(id=1, email=email)
        user_repository.get_by_email.return_value = mock_user

        with pytest.raises(BadRequestException):
            await user_controller.register(
                email=email,
                first_name="test",
                last_name="user",
                password="password123",
                role=UserRole.USER,
                activated=True,
            )

        user_repository.get_by_email.assert_called_once_with(email=email)

    async def test_update_success(self, user_controller, user_repository):
        user_uuid = uuid4()
        mock_user = User(id=1, uuid=user_uuid, email="test@example.com")
        user_repository.get_by_uuid.return_value = mock_user
        user_repository.update.return_value = mock_user

        result = await user_controller.update(user_uuid=user_uuid, email="newemail@example.com")

        assert result == mock_user
        assert mock_user.email == "newemail@example.com"
        user_repository.get_by_uuid.assert_called_once_with(uuid=user_uuid)
        user_repository.update.assert_called_once_with(model=mock_user, attributes={})

    async def test_update_user_not_found(self, user_controller, user_repository):
        user_uuid = uuid4()
        user_repository.get_by_uuid.return_value = None

        with pytest.raises(NotFoundException):
            await user_controller.update(user_uuid=user_uuid, email="newemail@example.com")

        user_repository.get_by_uuid.assert_called_once_with(uuid=user_uuid)

    async def test_delete_success(self, user_controller, user_repository):
        user_uuid = uuid4()
        mock_user = User(id=1, uuid=user_uuid, email="test@example.com")
        user_repository.get_by_uuid.return_value = mock_user

        await user_controller.delete(user_uuid=user_uuid)

        user_repository.get_by_uuid.assert_called_once_with(uuid=user_uuid)
        user_repository.delete.assert_called_once_with(model=mock_user)

    async def test_delete_user_not_found(self, user_controller, user_repository):
        user_uuid = uuid4()
        user_repository.get_by_uuid.return_value = None

        with pytest.raises(NotFoundException):
            await user_controller.delete(user_uuid=user_uuid)

        user_repository.get_by_uuid.assert_called_once_with(uuid=user_uuid)
