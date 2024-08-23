from uuid import UUID

from fastapi import APIRouter, Depends, status

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
async def get_user(uuid=UUID, user_controller: UserController = Depends(Factory().get_user_controller)) -> UserResponse:
    """
    Retrieve user by ID.
    """
    return await user_controller.get_by_uuid(uuid=uuid)


@user_router.post("/", status_code=status.HTTP_201_CREATED)
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


@user_router.put("/{id}")
async def update_user(
    uuid: UUID,
    update_user_request: UpdateUserRequest,
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> UserResponse:
    """
    Update a user.
    """
    return await user_controller.update(
        user_uuid=uuid,
        email=update_user_request.email,
        first_name=update_user_request.first_name,
        last_name=update_user_request.last_name,
        password=update_user_request.password,
    )


@user_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    uuid: UUID,
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> None:
    """
    Delete a user.
    """
    return await user_controller.delete(user_uuid=uuid)
