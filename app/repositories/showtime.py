from pydantic import UUID4
from sqlalchemy import Select, select
from sqlalchemy.orm import joinedload

from app.models import Movie, Showtime
from app.schemas.request import ShowtimeFilterParams
from core.repository import BaseRepository


class ShowtimeRepository(BaseRepository[Showtime]):
    """
    Showtime repository provides all the database operations for the Showtime model.
    """

    async def get_filtered_showtimes(
        self, filter_params: ShowtimeFilterParams, join_: set[str] | None = None
    ) -> tuple[list[Showtime], int]:
        """
        Retrieve showtimes by filter and their related movies.

        :param join_: Join relations.
        :param filter_params: showtime filter parameters.
        :return: a tuple of list of showtimes and the total count of matching users.
        """
        query = self._query(join_)

        if join_ and "movie" in join_:
            query = self._join_movie(query)

        if filter_params.start_time:
            query = query.filter(Showtime.start_time == filter_params.start_time)
        if filter_params.end_time:
            query = query.filter(Showtime.end_time == filter_params.end_time)

        if filter_params.created_from:
            query = query.filter(Showtime.created >= filter_params.created_from)
        if filter_params.created_to:
            query = query.filter(Showtime.created <= filter_params.created_to)

        if filter_params.updated_from:
            query = query.filter(Showtime.updated >= filter_params.updated_from)
        if filter_params.updated_to:
            query = query.filter(Showtime.updated <= filter_params.updated_to)

        order_column = Showtime.created if filter_params.order_by == "created" else Showtime.updated
        query = query.order_by(order_column)

        paginated_query = query.limit(filter_params.limit).offset(filter_params.offset)

        showtimes = await self._all(query=paginated_query)
        total = await self._count(query=query)

        return showtimes, total

    async def get_by_uuid(self, uuid: UUID4, join_: set[str] | None = None) -> Showtime | None:
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
