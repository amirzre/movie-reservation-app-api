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

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_movie(
        self,
        *,
        movie_uuid: UUID,
        title: str | None = None,
        description: str | None = None,
        genre: str | None = None,
        release_date: datetime | None = None,
        activated: bool | None = True,
    ) -> Movie:
        movie = await self.movie_repository.get_by_uuid(uuid=movie_uuid)
        if not movie:
            raise NotFoundException(message="Movie not found.")

        attributes = {}
        if title is not None:
            attributes["title"] = title
        if description is not None:
            attributes["description"] = description
        if genre is not None:
            attributes["genre"] = genre
        if release_date is not None:
            attributes["release_date"] = release_date
        if activated is not None:
            attributes["activated"] = activated

        return await self.movie_repository.update(model=movie, attributes=attributes)
