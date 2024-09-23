from uuid import UUID

from app.models import Showtime
from core.repository import BaseRepository


class ShowtimeRepository(BaseRepository[Showtime]):
    """
    Showtime repository provides all the database operations for the Showtime model.
    """

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
            return await self._all_unique(query)

        return await self._one_or_none(query)
