from fastapi import APIRouter

from .showtimes import showtime_router

showtimes_router = APIRouter()
showtimes_router.include_router(showtime_router, tags=["Showtimes"])

__all__ = ["showtime_router"]
