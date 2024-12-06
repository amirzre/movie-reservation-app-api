from uuid import UUID

from app.models import Showtime
from app.repositories import ShowtimeRepository
from app.schemas.request import CreateShowtimeRequest
from core.controller import BaseController
from core.db import Propagation, Transactional
from core.exceptions import NotFoundException


class ShowtimeController(BaseController[Showtime]):
    """
    Showtime controller provides all the logic operations for the Showtime model.
    """

    def __init__(self, showtime_repository: ShowtimeRepository):
        super().__init__(model=Showtime, repository=showtime_repository)
        self.showtime_repository = showtime_repository

    async def get_showtimes(self) -> list[Showtime]:
        return await self.showtime_repository.get_showtimes(join_={"movie"})

    async def get_showtime(self, *, showtime_uuid: UUID) -> Showtime:
        showtime = await self.showtime_repository.get_by_uuid(uuid=showtime_uuid)
        if not showtime:
            raise NotFoundException(message="Showtime not found.")
        return showtime

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_showtime(self, *, create_showtime_request: CreateShowtimeRequest) -> Showtime:
        movie = await self.showtime_repository.get_movie_by_id(
            id_=create_showtime_request.movie_id, join_={"showtimes"}
        )
        print("-----------------movie: ", movie)
        if not movie:
            raise NotFoundException(message="Movie not found.")

        return await self.showtime_repository.create(
            attributes={
                "start_time": create_showtime_request.start_time,
                "end_time": create_showtime_request.end_time,
                "available_seats": create_showtime_request.available_seats,
                "total_seats": create_showtime_request.total_seats,
                "movie_id": movie.uuid,
            }
        )
