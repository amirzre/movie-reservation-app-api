from uuid import UUID

from app.models import Showtime
from app.repositories import ShowtimeRepository
from core.controller import BaseController
from core.exceptions import NotFoundException


class ShowtimeController(BaseController[Showtime]):
    """
    Showtime controller provides all the logic operations for the Showtime model.
    """

    def __init__(self, showtime_repository: ShowtimeRepository):
        super().__init__(model=Showtime, repository=showtime_repository)
        self.showtime_repository = showtime_repository

    async def get_showtimes(self) -> list[Showtime]:
        return await self.showtime_repository.get_showtimes(join_={"movie"})

    async def get_showtime(self, showtime_uuid: UUID) -> Showtime:
        showtime = await self.showtime_repository.get_by_uuid(uuid=showtime_uuid)
        if not showtime:
            raise NotFoundException(message="Showtime not found.")
        return showtime
