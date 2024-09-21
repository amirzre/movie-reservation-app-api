from .auth import UserLoginRequest
from .movie import CreateMovieRequest, UpdateMovieRequest
from .user import RegisterUserRequest, UpdateUserRequest

__all__ = [
    "RegisterUserRequest",
    "UpdateUserRequest",
    "UserLoginRequest",
    "CreateMovieRequest",
    "UpdateMovieRequest",
]
