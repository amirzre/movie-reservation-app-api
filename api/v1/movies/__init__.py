from fastapi import APIRouter

from .movies import movie_router

movies_router = APIRouter()
movies_router.include_router(movie_router, tags=["Movies"])

__all__ = ["movie_router"]
