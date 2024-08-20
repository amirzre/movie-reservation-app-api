from uuid import UUID

from app.models import User
from app.models.user import UserRole
from app.repositories import UserRepository
from core.controller import BaseController
from core.db import Propagation, Transactional
from core.exceptions import BadRequestException, NotFoundException
from core.security import PasswordHandler


class UserController(BaseController[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(model=User, repository=user_repository)
        self.user_repository = user_repository

    async def get_user(self, *, user_uuid: UUID) -> User:
        user = await self.user_repository.get_by_uuid(uuid=user_uuid)
        if not user:
            raise NotFoundException(message="User not found.")
        return user

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

    @Transactional(propagation=Propagation.REQUIRED)
    async def update(
        self,
        *,
        user_uuid: UUID,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        password: str | None = None,
    ) -> User:
        user = await self.user_repository.get_by_uuid(uuid=user_uuid)
        if not user:
            raise NotFoundException(message="User not found.")

        if email is not None:
            user.email = email
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if password is not None:
            user.password = PasswordHandler.hash(password=password)

        return await self.user_repository.update(model=user, attributes={})

    async def delete(self, *, user_uuid: UUID) -> None:
        user = await self.user_repository.get_by_uuid(uuid=user_uuid)
        if not user:
            raise NotFoundException(message="User not found.")

        return await self.user_repository.delete(model=user)
