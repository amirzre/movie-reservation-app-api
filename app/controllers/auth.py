from redis.asyncio import client

from app.models import User
from app.repositories import UserRepository
from app.schemas.extras import Token
from core.controller import BaseController
from core.exceptions import BadRequestException
from core.security import JWTHandler, PasswordHandler


class AuthController(BaseController[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(model=User, repository=user_repository)
        self.user_repository = user_repository

    async def login(self, *, email: str, password: str, cache: client.Redis) -> Token:
        user = await self.user_repository.get_by_email(email=email)
        if not user:
            raise BadRequestException(message="Invalid credentials.")
        if not PasswordHandler.verify(user.password, password):
            raise BadRequestException(message="Invalid credentials.")
        if user.activated is False:
            raise BadRequestException(message="The user is inactive.")

        refresh_token = JWTHandler.encode_refresh_token(
            payload={"sub": "refresh_token", "verify": str(user.uuid), "role": user.role}
        )
        access_token = JWTHandler.encode(payload={"uuid": str(user.uuid), "role": user.role})

        await cache.set(name=refresh_token, value=str(user.uuid), ex=JWTHandler.refresh_token_expire)
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )
