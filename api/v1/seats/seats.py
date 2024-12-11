from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.controllers import SeatController
from app.schemas.extras import PaginationResponse
from app.schemas.request import SeatFilterParams
from app.schemas.response import SeatResponse
from core.factory import Factory
from core.fastapi.dependencies import get_authenticated_user

seat_router = APIRouter()


@seat_router.get("/", dependencies=[Depends(get_authenticated_user)])
async def get_seats(
    filter_params: Annotated[SeatFilterParams, Query()],
    seat_controller: SeatController = Depends(Factory().get_seat_controller),
) -> PaginationResponse[SeatResponse]:
    """
    Retrieve seats.
    """
    return await seat_controller.get_seats(filter_params=filter_params)
