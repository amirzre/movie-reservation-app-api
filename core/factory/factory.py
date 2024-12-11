from functools import partial

from fastapi import Depends

from app.controllers import AuthController, MovieController, SeatController, ShowtimeController, UserController
from app.models import Movie, Seat, Showtime, User
from app.repositories import MovieRepository, SeatRepository, ShowtimeRepository, UserRepository
from core.db import get_session


class Factory:
    """
    This is the factory container that will instantiate all the controllers and
    repositories which can be accessed by the rest of the application.
    """

    user_repository = partial(UserRepository, User)
    movie_repository = partial(MovieRepository, Movie)
    showtime_repository = partial(ShowtimeRepository, Showtime)
    seat_repository = partial(SeatRepository, Seat)

    def get_user_controller(self, db_session=Depends(get_session)):
        return UserController(user_repository=self.user_repository(db_session=db_session))

    def get_auth_controller(self, db_session=Depends(get_session)):
        return AuthController(user_repository=self.user_repository(db_session=db_session))

    def get_movie_controller(self, db_session=Depends(get_session)):
        return MovieController(movie_repository=self.movie_repository(db_session=db_session))

    def get_showtime_controller(self, db_session=Depends(get_session)):
        return ShowtimeController(showtime_repository=self.showtime_repository(db_session=db_session))

    def get_seat_controller(self, db_session=Depends(get_session)):
        return SeatController(seat_repository=self.seat_repository(db_session=db_session))
