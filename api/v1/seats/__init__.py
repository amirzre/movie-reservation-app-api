from fastapi import APIRouter

from .seats import seat_router

seats_router = APIRouter()
seats_router.include_router(seat_router, tags=["Seats"])

__all__ = ["seats_router"]
