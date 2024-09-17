from app.models import Movie
from app.repositories import MovieRepository
from core.controller import BaseController


class MovieController(BaseController[Movie]):
    """
    Movie controller provides all the logic operations for the Movie model.
    """

    def __init__(self, movie_repository: MovieRepository):
        super().__init__(model=Movie, repository=movie_repository)
        self.movie_repository = movie_repository

    ...
