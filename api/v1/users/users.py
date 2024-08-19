from fastapi import APIRouter, Depends

from app.controllers import UserController
from app.schemas.request import RegisterUserRequest
from app.schemas.response import UserResponse
from core.factory import Factory

user_router = APIRouter()


@user_router.post("/", status_code=201)
async def register_user(
    register_user_request: RegisterUserRequest,
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> UserResponse:
    """
    Register new user.
    """
    return await user_controller.register(
        email=register_user_request.email,
        first_name=register_user_request.first_name,
        last_name=register_user_request.last_name,
        password=register_user_request.password,
        role=register_user_request.role,
        activated=register_user_request.activated,
    )
