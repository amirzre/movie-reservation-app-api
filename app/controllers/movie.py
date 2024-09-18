from datetime import datetime
from uuid import UUID

from app.models import Movie
from app.repositories import MovieRepository
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

    async def get_movie(self, *, movie_uuid: UUID) -> Movie:
        movie = await self.movie_repository.get_by_uuid(uuid=movie_uuid)
        if not movie:
            raise NotFoundException(message="Movie not found.")
        return movie

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_movie(
        self,
        *,
        title: str,
        description: str | None,
        genre: str,
        release_date: datetime,
        activated: bool | None = True,
    ) -> Movie:
        return await self.movie_repository.create(
            attributes={
                "title": title,
                "description": description,
                "genre": genre,
                "release_date": release_date,
                "activated": activated,
            }
        )
