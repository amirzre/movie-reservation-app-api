from uuid import UUID

from fastapi import APIRouter, Depends

from app.controllers import MovieController
from app.schemas.response import MovieResponse
from core.factory import Factory

movie_router = APIRouter()


@movie_router.get("/")
async def get_movies(
    movie_controller: MovieController = Depends(Factory().get_movie_controller),
) -> list[MovieResponse]:
    """
    Retrieve movies.
    """
    return await movie_controller.get_all()


@movie_router.get("/{id}")
async def get_movie(
    id: UUID,
    movie_controller: MovieController = Depends(Factory().get_movie_controller),
) -> MovieResponse:
    """
    Retrieve movie by ID.
    """
    return await movie_controller.get_movie(movie_uuid=id)
