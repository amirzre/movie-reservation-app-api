from app.models import Showtime
from app.repositories import ShowtimeRepository
from core.controller import BaseController


class ShowtimeController(BaseController[Showtime]):
    """
    Showtime controller provides all the logic operations for the Showtime model.
    """

    def __init__(self, showtime_repository: ShowtimeRepository):
        super().__init__(model=Showtime, repository=showtime_repository)
        self.showtime_repository = showtime_repository

    ...
