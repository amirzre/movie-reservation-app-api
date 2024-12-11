from app.models import Seat
from app.repositories import SeatRepository
from app.schemas.extras import PaginationResponse
from app.schemas.request import SeatFilterParams
from app.schemas.response import SeatResponse
from core.controller import BaseController


class SeatController(BaseController[Seat]):
    """
    Seat controller provides all the logic operations for the seat model.
    """

    def __init__(self, seat_repository: SeatRepository):
        super().__init__(model=Seat, repository=seat_repository)
        self.seat_repository = seat_repository

    async def get_seats(self, *, filter_params: SeatFilterParams) -> PaginationResponse[SeatResponse]:
        
        seats, total = await self.seat_repository.get_filtered_seats(filter_params=filter_params, join_={"showtime"})

        return PaginationResponse[SeatResponse](
            limit=filter_params.limit, offset=filter_params.offset, total=total, items=seats
        )
