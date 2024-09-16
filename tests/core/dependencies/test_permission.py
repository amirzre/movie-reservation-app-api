import pytest

from app.models import User, UserRole
from core.exceptions import ForbiddenException
from core.fastapi.dependencies.permission import RoleChecker


@pytest.mark.asyncio
class TestRoleChecker:
    @pytest.fixture
    def mock_user_admin(self):
        return User(id=1, role=UserRole.ADMIN, activated=True)

    @pytest.fixture
    def mock_user_non_admin(self):
        return User(id=2, role=UserRole.USER, activated=True)

    @pytest.fixture
    def role_checker_admin(self):
        return RoleChecker(allowed_roles=[UserRole.ADMIN])

    @pytest.fixture
    def role_checker_empty(self):
        return RoleChecker(allowed_roles=[])

    async def test_user_with_allowed_role(self, mock_user_admin, role_checker_admin):
        is_allowed = role_checker_admin(user=mock_user_admin)
        assert is_allowed is True

    async def test_user_without_allowed_role(self, mock_user_non_admin, role_checker_admin):
        with pytest.raises(ForbiddenException):
            role_checker_admin(user=mock_user_non_admin)

    async def test_user_with_empty_allowed_roles(self, mock_user_admin, role_checker_empty):
        with pytest.raises(ForbiddenException):
            role_checker_empty(user=mock_user_admin)

    async def test_user_with_none_role(self, role_checker_admin):
        user = User(id=3, role=None, activated=True)
        with pytest.raises(ForbiddenException):
            role_checker_admin(user=user)
