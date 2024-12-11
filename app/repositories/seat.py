from pydantic import UUID4

from app.models import Seat
from core.repository import BaseRepository


class SeatRepository(BaseRepository[Seat]):
    """
    Seat repository provides all the database operations for the Seat model.
    """

    async def get_by_uuid(self, uuid: UUID4) -> Seat | None:
        """
        Get seat by uuid.

        :param: uuid: Seat uuid.
        :param join_: Join relation.
        :return: Seat.
        """
        query = self._query()
        query = query.filter(Seat.uuid == uuid)

        return await self._one_or_none(query)
