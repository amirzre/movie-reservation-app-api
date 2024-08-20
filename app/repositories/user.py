from uuid import UUID

from app.models import User
from core.repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    User repository provides all the database operations for the User model.
    """

    async def get_by_email(self, email: str, join_: set[str] | None = None) -> User | None:
        """
        Get user by email.

        :param email: Email.
        :param join_: Join relations.
        :return: User.
        """
        query = self._query(join_)
        query = query.filter(User.email == email)

        if join_ is not None:
            return await self._all_unique(query)

        return await self._one_or_none(query)

    async def get_by_uuid(self, uuid: UUID, join_: set[str] | None = None) -> User | None:
        """
        Get user by uuid.

        :param uuid: User uuid.
        :param join_: Join relations.
        :return: User.
        """
        query = self._query(join_)
        query = query.filter(User.uuid == uuid)

        if join_ is not None:
            return await self._all_unique(query)

        return await self._one_or_none(query)
