from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.controllers import MovieController
from app.schemas.request import CreateMovieRequest, UpdateMovieRequest
from app.schemas.response import MovieResponse
from core.factory import Factory
from core.fastapi.dependencies import ADMINISTRATIVE, RoleChecker

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


@movie_router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(RoleChecker(ADMINISTRATIVE))])
async def create_movie(
    create_movie_request: CreateMovieRequest,
    movie_controller: MovieController = Depends(Factory().get_movie_controller),
) -> MovieResponse:
    """
    Create new movie.
    """
    return await movie_controller.create_movie(
        title=create_movie_request.title,
        description=create_movie_request.description,
        genre=create_movie_request.genre,
        release_date=create_movie_request.release_date,
        activated=create_movie_request.activated,
    )


@movie_router.put("/{id}", status_code=status.HTTP_200_OK, dependencies=[Depends(RoleChecker(ADMINISTRATIVE))])
async def update_movie(
    id: UUID,
    update_movie_request: UpdateMovieRequest,
    movie_controller: MovieController = Depends(Factory().get_movie_controller),
) -> MovieResponse:
    """
    Update movie.
    """
    return await movie_controller.update_movie(
        movie_uuid=id,
        title=update_movie_request.title,
        description=update_movie_request.description,
        genre=update_movie_request.genre,
        release_date=update_movie_request.release_date,
        activated=update_movie_request.activated,
    )
