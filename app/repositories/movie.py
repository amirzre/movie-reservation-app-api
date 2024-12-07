from pydantic import UUID4

from app.models import Movie
from app.schemas.request import MovieFilterParams
from core.repository import BaseRepository


class MovieRepository(BaseRepository[Movie]):
    """
    Movie repository provides all the database operations for the Movie model.
    """

    async def get_by_uuid(self, uuid: UUID4) -> Movie | None:
        """
        Get movie by uuid.

        :param uuid: Movie uuid.
        :param join_: Join relations.
        :return: Movie.
        """
        query = self._query()
        query = query.filter(Movie.uuid == uuid)

        return await self._one_or_none(query)

    async def get_filtered_movies(self, filter_params: MovieFilterParams) -> tuple[list[Movie], int]:
        """
        Get movies by filter and return the total count.

        :param filter_params: movie filter parameters.
        :return: a tuple of list of movies and the total count of matching movies.
        """
        query = self._query()

        if filter_params.title:
            query = query.filter(Movie.title.contains(filter_params.title))
        if filter_params.genre:
            query = query.filter(Movie.genre.contains(filter_params.genre))
        if filter_params.release_date:
            query = query.filter(Movie.release_date == filter_params.release_date)
        if filter_params.activated:
            query = query.filter(Movie.activated == filter_params.activated)

        if filter_params.created_from:
            query = query.filter(Movie.created >= filter_params.created_from)
        if filter_params.created_to:
            query = query.filter(Movie.created <= filter_params.created_to)

        if filter_params.updated_from:
            query = query.filter(Movie.updated >= filter_params.updated_from)
        if filter_params.updated_to:
            query = query.filter(Movie.updated <= filter_params.updated_to)

        order_column = Movie.created if filter_params.order_by == "created" else Movie.updated
        query = query.order_by(order_column)

        paginated_query = query.limit(filter_params.limit).offset(filter_params.offset)

        movies = await self._all(query=paginated_query)
        total = await self._count(query=query)

        return movies, total
