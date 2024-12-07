from pydantic import UUID4

from app.models import Showtime
from app.repositories import ShowtimeRepository
from app.schemas.extras import PaginationResponse
from app.schemas.request import CreateShowtimeRequest, ShowtimeFilterParams, UpdateShowtimeRequest
from app.schemas.response import MovieResponse, ShowtimeResponse
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

    async def get_showtimes(self, *, filter_params: ShowtimeFilterParams) -> PaginationResponse[ShowtimeResponse]:
        showtimes, total = await self.showtime_repository.get_filtered_showtimes(
            filter_params=filter_params, join_={"movie"}
        )
        return PaginationResponse[ShowtimeResponse](
            limit=filter_params.limit, offset=filter_params.offset, total=total, items=showtimes
        )

    async def get_showtime(self, *, showtime_uuid: UUID4) -> ShowtimeResponse:
        showtime = await self.showtime_repository.get_by_uuid(uuid=showtime_uuid, join_={"movie"})
        if not showtime:
            raise NotFoundException(message="Showtime not found.")
        return ShowtimeResponse(
            id=showtime.id,
            uuid=showtime.uuid,
            start_time=showtime.start_time,
            end_time=showtime.end_time,
            available_seats=showtime.available_seats,
            total_seats=showtime.total_seats,
            movie=showtime.movie,
        )

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_showtime(self, *, create_showtime_request: CreateShowtimeRequest) -> ShowtimeResponse:
        movie = await self.showtime_repository.get_movie_by_id(
            id_=create_showtime_request.movie_id, join_={"showtimes"}
        )
        if not movie:
            raise NotFoundException(message="Movie not found.")

        created_showtime = await self.showtime_repository.create(attributes=create_showtime_request)
        return ShowtimeResponse(
            id=created_showtime.id,
            uuid=created_showtime.uuid,
            start_time=created_showtime.start_time,
            end_time=created_showtime.end_time,
            available_seats=created_showtime.available_seats,
            total_seats=created_showtime.total_seats,
            movie=MovieResponse(
                id=movie.id,
                uuid=movie.uuid,
                title=movie.title,
                description=movie.description,
                genre=movie.genre,
                release_date=movie.release_date,
                activated=movie.activated,
            ),
        )

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_showtime(
        self, *, showtime_uuid: UUID4, update_showtime_request: UpdateShowtimeRequest
    ) -> ShowtimeResponse:
        showtime = await self.showtime_repository.get_by_uuid(uuid=showtime_uuid, join_={"movie"})
        if not showtime:
            raise NotFoundException(message="Showtime not found.")

        updated_showtime = await self.showtime_repository.update(model=showtime, attributes=update_showtime_request)

        return ShowtimeResponse(
            id=updated_showtime.id,
            uuid=updated_showtime.uuid,
            start_time=updated_showtime.start_time,
            end_time=updated_showtime.end_time,
            available_seats=updated_showtime.available_seats,
            total_seats=updated_showtime.total_seats,
            movie=showtime.movie,
        )

    @Transactional(propagation=Propagation.REQUIRED)
    async def delete_showtime(self, showtime_uuid: UUID4) -> None:
        showtime = await self.showtime_repository.get_by_uuid(uuid=showtime_uuid)
        if not showtime:
            raise NotFoundException(message="Showtime not found.")

        return await self.showtime_repository.delete(model=showtime)
