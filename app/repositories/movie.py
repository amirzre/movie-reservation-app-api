from uuid import UUID

from app.models import Movie
from core.repository import BaseRepository


class MovieRepository(BaseRepository[Movie]):
    """
    Movie repository provides all the database operations for the Movie model.
    """

    async def get_by_uuid(self, uuid: UUID, join_: set[str] | None = None) -> Movie | None:
        """
        Get movie by uuid.

        :param uuid: Movie uuid.
        :param join_: Join relations.
        :return: Movie.
        """
        query = self._query(join_)
        query = query.filter(Movie.uuid == uuid)

        if join_ is not None:
            return await self._all_unique(query)

        return await self._one_or_none(query)
