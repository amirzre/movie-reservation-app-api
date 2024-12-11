from fastapi import APIRouter

from .auth import auth_routers
from .movies import movies_router
from .seats import seats_router
from .showtimes import showtimes_router
from .users import users_router

v1_router = APIRouter()
v1_router.include_router(auth_routers, prefix="/auth")
v1_router.include_router(users_router, prefix="/users")
v1_router.include_router(movies_router, prefix="/movies")
v1_router.include_router(showtimes_router, prefix="/showtimes")
v1_router.include_router(seats_router, prefix="/seats")
