from datetime import datetime, timedelta

import jwt

from core.config import config
from core.exceptions import CustomException


class JWTDecodeError(CustomException):
    code = 401
    message = "Invalid token"


class JWTExpiredError(CustomException):
    code: 401
    message = "Token expired"


class JWTHandler:
    secret_key = config.SECRET_KEY
    algorithm = config.JWT_ALGORITHM
    expire = config.JWT_EXPIRE_MINUTES

    @staticmethod
    def encode(payload: dict) -> str:
        expire = datetime.now() + timedelta(minutes=JWTHandler.expire)
        payload.update({"exp": expire})
        return jwt.encode(
            payload=payload,
            key=JWTHandler.secret_key,
            algorithm=JWTHandler.algorithm,
        )

    @staticmethod
    def decode(token: str) -> dict:
        try:
            return jwt.decode(
                token=token,
                key=JWTHandler.secret_key,
                algorithms=[JWTHandler.algorithm],
            )
        except jwt.exceptions.DecodeError as exception:
            raise JWTDecodeError() from exception
        except jwt.exceptions.ExpiredSignatureError as exception:
            raise JWTExpiredError() from exception

    @staticmethod
    def decode_expired(token: str) -> dict:
        try:
            return jwt.decode(
                token=token,
                key=JWTHandler.secret_key,
                algorithms=[JWTHandler.algorithm],
                options={"verify_exp": False},
            )
        except jwt.exceptions.DecodeError as exception:
            raise JWTDecodeError() from exception
