from fastapi import APIRouter, Depends

from app.controllers import ShowtimeController
from app.schemas.response import ShowtimeResponse
from core.factory import Factory
from core.fastapi.dependencies import get_authenticated_user

showtime_router = APIRouter()


@showtime_router.get("/", dependencies=[Depends(get_authenticated_user)])
async def get_showtimes(
    showtime_controller: ShowtimeController = Depends(Factory().get_showtime_controller)
) -> list[ShowtimeResponse]:
    """
    Retrieve showtimes.
    """
    ...
    return await showtime_controller.get_showtimes()
