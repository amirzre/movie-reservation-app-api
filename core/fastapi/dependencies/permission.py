from typing import Annotated

from fastapi import Depends

from app.models import User, UserRole
from core.exceptions import ForbiddenException

from .current_user import get_current_user

ADMINISTRATIVE = [UserRole.ADMIN]


class RoleChecker:
    def __init__(self, allowed_roles: list[UserRole]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, user: Annotated[User, Depends(get_current_user)]) -> bool:
        if user.role in self.allowed_roles:
            return True
        raise ForbiddenException(message="You do not have permission to perform this operation.")
