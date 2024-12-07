from pydantic import UUID4

from app.models import Movie
from app.repositories import MovieRepository
from app.schemas.extras import PaginationResponse
from app.schemas.request import CreateMovieRequest, MovieFilterParams, UpdateMovieRequest
from app.schemas.response import MovieResponse
from core.controller import BaseController
from core.db import Propagation, Transactional
from core.exceptions import NotFoundException


class MovieController(BaseController[Movie]):
    """
    Movie controller provides all the logic operations for the Movie model.
    """

    def __init__(self, movie_repository: MovieRepository):
        super().__init__(model=Movie, repository=movie_repository)
        self.movie_repository = movie_repository

    async def get_movies(self, *, filter_params: MovieFilterParams) -> PaginationResponse[MovieResponse]:
        movies, total = await self.movie_repository.get_filtered_movies(filter_params=filter_params)
        return PaginationResponse[MovieResponse](
            limit=filter_params.limit, offset=filter_params.offset, total=total, items=movies
        )

    async def get_movie(self, *, movie_uuid: UUID4) -> MovieResponse:
        movie = await self.movie_repository.get_by_uuid(uuid=movie_uuid)
        if not movie:
            raise NotFoundException(message="Movie not found.")
        return MovieResponse(
            id=movie.id,
            uuid=movie.uuid,
            title=movie.title,
            description=movie.description,
            genre=movie.genre,
            release_date=movie.release_date,
            activated=movie.activated,
        )

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_movie(self, *, create_movie_request: CreateMovieRequest) -> MovieResponse:
        created_movie = await self.movie_repository.create(attributes=create_movie_request)
        return MovieResponse(
            id=created_movie.id,
            uuid=created_movie.uuid,
            title=created_movie.title,
            description=created_movie.description,
            genre=created_movie.genre,
            release_date=created_movie.release_date,
            activated=created_movie.activated,
        )

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_movie(self, *, movie_uuid: UUID4, update_movie_request: UpdateMovieRequest) -> MovieResponse:
        movie = await self.movie_repository.get_by_uuid(uuid=movie_uuid)
        if not movie:
            raise NotFoundException(message="Movie not found.")

        updated_movie = await self.movie_repository.update(model=movie, attributes=update_movie_request)
        return MovieResponse(
            id=updated_movie.id,
            uuid=updated_movie.uuid,
            title=updated_movie.title,
            description=updated_movie.description,
            genre=updated_movie.genre,
            release_date=updated_movie.release_date,
            activated=updated_movie.activated,
        )

    async def delete_movie(self, *, movie_uuid: UUID4) -> None:
        movie = await self.movie_repository.get_by_uuid(uuid=movie_uuid)
        if not movie:
            raise NotFoundException(message="Movie not found.")

        return await self.movie_repository.delete(model=movie)
