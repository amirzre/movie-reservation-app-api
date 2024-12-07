from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.orm import joinedload

from app.models import Movie, Showtime
from core.repository import BaseRepository


class ShowtimeRepository(BaseRepository[Showtime]):
    """
    Showtime repository provides all the database operations for the Showtime model.
    """

    async def get_showtimes(self, join_: set[str] | None = None) -> list[Showtime]:
        """
        Retrieve all showtimes with their related movies.

        :param join_: Join relations.
        :return: Showtimes list.
        """
        query = self._query(join_)

        if join_ and "movie" in join_:
            query = self._join_movie(query)

        return await self._all(query)

    async def get_by_uuid(self, uuid: UUID, join_: set[str] | None = None) -> Showtime | None:
        """
        Get showtime by uuid.

        :param uuid: Showtime uuid.
        :param join_: Join relations.
        :return: Showtime.
        """
        query = self._query(join_)
        query = query.filter(Showtime.uuid == uuid)

        if join_ is not None:
            query = self._join_movie(query)

        return await self._one_or_none(query)

    async def get_movie_by_id(self, id_: int, join_: set[str] | None = None) -> Movie:
        """
        Get Moive by id.

        :param id: Movie id.
        :param join_: Join relations.
        :return: Movie.
        """
        query = select(Movie).filter(Movie.id == id_)

        if join_ is not None and "showtime" in join_:
            query = query.options(joinedload(Movie.showtimes))

        return await self._one_or_none(query)

    def _join_movie(self, query: Select) -> Select:
        """
        Join the moive relationship.

        :param query: The query to join.
        :return: The joined query.
        """
        return query.options(joinedload(Showtime.movie))
