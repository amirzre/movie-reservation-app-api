from fastapi import APIRouter, Depends, status
from pydantic import UUID4

from app.controllers import UserController
from app.schemas.request import RegisterUserRequest, UpdateUserRequest
from app.schemas.response import UserResponse
from core.factory import Factory
from core.fastapi.dependencies import ADMINISTRATIVE, RoleChecker

user_router = APIRouter()


@user_router.get("/", dependencies=[Depends(RoleChecker(ADMINISTRATIVE))])
async def get_users(user_controller: UserController = Depends(Factory().get_user_controller)) -> list[UserResponse]:
    """
    Retrieve users.
    """
    return await user_controller.get_all()


@user_router.get("/{id}", dependencies=[Depends(RoleChecker(ADMINISTRATIVE))])
async def get_user(id=UUID4, user_controller: UserController = Depends(Factory().get_user_controller)) -> UserResponse:
    """
    Retrieve user by ID.
    """
    return await user_controller.get_user(user_uuid=id)


@user_router.post("/", status_code=status.HTTP_201_CREATED)
async def register_user(
    register_user_request: RegisterUserRequest,
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> UserResponse:
    """
    Register new user.
    """
    return await user_controller.register_user(register_user_request=register_user_request)


@user_router.put("/{id}")
async def update_user(
    id: UUID4,
    update_user_request: UpdateUserRequest,
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> UserResponse:
    """
    Update a user.
    """
    return await user_controller.update_user(user_uuid=id, update_user_request=update_user_request)


@user_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: UUID4,
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> None:
    """
    Delete a user.
    """
    return await user_controller.delete_user(user_uuid=id)
