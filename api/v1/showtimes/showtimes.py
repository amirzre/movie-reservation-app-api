from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from pydantic import UUID4

from app.controllers import ShowtimeController
from app.schemas.extras import PaginationResponse
from app.schemas.request import CreateShowtimeRequest, ShowtimeFilterParams, UpdateShowtimeRequest
from app.schemas.response import ShowtimeResponse
from core.factory import Factory
from core.fastapi.dependencies import ADMINISTRATIVE, RoleChecker, get_authenticated_user

showtime_router = APIRouter()


@showtime_router.get("/", dependencies=[Depends(get_authenticated_user)])
async def get_showtimes(
    filter_params: Annotated[ShowtimeFilterParams, Query()],
    showtime_controller: ShowtimeController = Depends(Factory().get_showtime_controller),
) -> PaginationResponse[ShowtimeResponse]:
    """
    Retrieve showtimes.
    """
    return await showtime_controller.get_showtimes(filter_params=filter_params)


@showtime_router.get("/{id}", dependencies=[Depends(get_authenticated_user)])
async def get_showtime(
    id: UUID4,
    showtime_controller: ShowtimeController = Depends(Factory().get_showtime_controller),
) -> ShowtimeResponse:
    """
    Retrieve an showtime.
    """
    return await showtime_controller.get_showtime(showtime_uuid=id)


@showtime_router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(RoleChecker(ADMINISTRATIVE))])
async def create_showtime(
    create_showtime_request: CreateShowtimeRequest,
    showtime_controller: ShowtimeController = Depends(Factory().get_showtime_controller),
) -> ShowtimeResponse:
    """
    Create new showtime.
    """
    return await showtime_controller.create_showtime(create_showtime_request=create_showtime_request)


@showtime_router.put("/{id}", dependencies=[Depends(RoleChecker(ADMINISTRATIVE))])
async def update_showtime(
    id: UUID4,
    update_showtime_request: UpdateShowtimeRequest,
    showtime_controller: ShowtimeController = Depends(Factory().get_showtime_controller),
) -> ShowtimeResponse:
    """
    Update a showtime.
    """
    return await showtime_controller.update_showtime(showtime_uuid=id, update_showtime_request=update_showtime_request)
