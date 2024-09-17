from app.models import Movie
from core.repository import BaseRepository


class MovieRepository(BaseRepository[Movie]):
    """
    Movie repository provides all the database operations for the Movie model.
    """

    ...
