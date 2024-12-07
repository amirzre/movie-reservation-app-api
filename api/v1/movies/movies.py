from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from pydantic import UUID4

from app.controllers import MovieController
from app.schemas.extras import PaginationResponse
from app.schemas.request import CreateMovieRequest, MovieFilterParams, UpdateMovieRequest
from app.schemas.response import MovieResponse
from core.factory import Factory
from core.fastapi.dependencies import ADMINISTRATIVE, RoleChecker, get_authenticated_user

movie_router = APIRouter()


@movie_router.get("/", dependencies=[Depends(get_authenticated_user)])
async def get_movies(
    filter_params: Annotated[MovieFilterParams, Query()],
    movie_controller: MovieController = Depends(Factory().get_movie_controller),
) -> PaginationResponse[MovieResponse]:
    """
    Retrieve movies.
    """
    return await movie_controller.get_movies(filter_params=filter_params)


@movie_router.get("/{id}", dependencies=[Depends(get_authenticated_user)])
async def get_movie(
    id: UUID4,
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
    return await movie_controller.create_movie(create_movie_request=create_movie_request)


@movie_router.put("/{id}", status_code=status.HTTP_200_OK, dependencies=[Depends(RoleChecker(ADMINISTRATIVE))])
async def update_movie(
    id: UUID4,
    update_movie_request: UpdateMovieRequest,
    movie_controller: MovieController = Depends(Factory().get_movie_controller),
) -> MovieResponse:
    """
    Update a movie.
    """
    return await movie_controller.update_movie(movie_uuid=id, update_movie_request=update_movie_request)


@movie_router.delete(
    "/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(RoleChecker(ADMINISTRATIVE))]
)
async def delete_movie(
    id: UUID4,
    movie_controller: MovieController = Depends(Factory().get_movie_controller),
) -> None:
    """
    Delete a movie.
    """
    return await movie_controller.delete_movie(movie_uuid=id)
