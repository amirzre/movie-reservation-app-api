from app.models import Seat
from app.repositories import SeatRepository
from core.controller import BaseController


class SeatController(BaseController[Seat]):
    """
    Seat controller provides all the logic operations for the seat model.
    """

    def __init__(self, seat_repository: SeatRepository):
        super().__init__(model=Seat, repository=seat_repository)
        self.seat_repository = seat_repository
