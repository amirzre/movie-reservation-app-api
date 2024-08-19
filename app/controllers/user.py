from app.models import User
from app.models.user import UserRole
from app.repositories import UserRepository
from core.controller import BaseController
from core.db import Propagation, Transactional
from core.exceptions import BadRequestException
from core.security import PasswordHandler


class UserController(BaseController[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(model=User, repository=user_repository)
        self.user_repository = user_repository

    @Transactional(propagation=Propagation.REQUIRED)
    async def register(
        self,
        *,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        role: UserRole | None,
        activated: bool | None,
    ) -> User:
        user = await self.user_repository.get_by_email(email=email)
        if user:
            raise BadRequestException(message="User already exists with this email.")

        password = PasswordHandler.hash(password=password)

        return await self.user_repository.create(
            {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "role": role,
                "activated": activated,
                "password": password,
            }
        )
