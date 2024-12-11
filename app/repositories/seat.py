from pydantic import UUID4

from app.models import Seat
from app.schemas.request import SeatFilterParams
from core.repository import BaseRepository


class SeatRepository(BaseRepository[Seat]):
    """
    Seat repository provides all the database operations for the Seat model.
    """

    async def get_filtered_seats(self, filter_params: SeatFilterParams) -> tuple[list[Seat], int]:
        """
        Retrieve seats by filter.

        :param filter_params: showtime filter parameters.
        :param join_: Join relations.
        :return: a tuple of list of seats and the total count of matching users.
        """
        query = self._query()

        if filter_params.seat_number:
            query = query.filter(Seat.seat_number == filter_params.seat_number)
        if filter_params.reserved:
            query = query.filter(Seat.reserved == filter_params.reserved)

        if filter_params.created_from:
            query = query.filter(Seat.created >= filter_params.created_from)
        if filter_params.created_to:
            query = query.filter(Seat.created <= filter_params.created_to)

        if filter_params.updated_from:
            query = query.filter(Seat.updated >= filter_params.updated_from)
        if filter_params.updated_to:
            query = query.filter(Seat.updated <= filter_params.updated_to)

        order_column = Seat.created if filter_params.order_by == "created" else Seat.updated
        query = query.order_by(order_column)

        paginated_query = query.limit(filter_params.limit).offset(filter_params.offset)

        seats = await self._all(query=paginated_query)
        total = await self._count(query=query)

        return seats, total

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
