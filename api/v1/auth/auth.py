from fastapi import APIRouter, Depends, Request, Response, status
from redis.asyncio import client

from app.controllers import AuthController
from app.schemas.request import UserLoginRequest
from core.exceptions import NotFoundException
from core.factory import Factory
from core.fastapi.dependencies import get_cache, get_current_user_with_refresh_token
from core.security import JWTHandler

auth_router = APIRouter()


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    response: Response,
    login_user_request: UserLoginRequest,
    cache: client.Redis = Depends(get_cache),
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> None:
    """
    Login user.
    """
    tokens = await auth_controller.login(
        email=login_user_request.email,
        password=login_user_request.password,
        cache=cache,
    )

    response.set_cookie(
        key="Access-Token",
        value=tokens.access_token,
        secure=True,
        httponly=True,
        samesite="strict",
        expires=JWTHandler.token_expiration(tokens.access_token),
    )
    response.set_cookie(
        key="Refresh-Token",
        value=tokens.refresh_token,
        secure=True,
        httponly=True,
        samesite="strict",
        expires=JWTHandler.token_expiration(tokens.refresh_token),
    )


@auth_router.post(
    "/refresh", status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user_with_refresh_token)]
)
async def refresh(
    request: Request,
    response: Response,
    cache: client.Redis = Depends(get_cache),
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> None:
    """
    Retrieve new access and refresh token.
    """
    tokens = await auth_controller.refresh(
        old_refresh_token=request.cookies.get("Refresh-Token", ""),
        cache=cache,
    )
    if not tokens.access_token:
        raise NotFoundException(message="Access token not found.")

    response.set_cookie(
        key="Access-Token",
        value=tokens.access_token,
        secure=True,
        httponly=True,
        samesite="strict",
        expires=JWTHandler.token_expiration(tokens.access_token),
    )
    response.set_cookie(
        key="Refresh-Token",
        value=tokens.refresh_token,
        secure=True,
        httponly=True,
        samesite="strict",
        expires=JWTHandler.token_expiration(tokens.refresh_token),
    )
