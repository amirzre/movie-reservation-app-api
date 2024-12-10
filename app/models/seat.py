from uuid import uuid4

from pydantic import UUID4
from sqlalchemy import UUID, BigInteger, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base
from core.db.mixins import TimestampMixin


class Seat(Base, TimestampMixin):
    __tablename__ = "seats"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    uuid: Mapped[UUID4] = mapped_column(UUID, unique=True, index=True, default=uuid4)
    seat_number: Mapped[str] = mapped_column(String(10), nullable=False)
    reserved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    showtime_id: Mapped[int] = mapped_column(Integer, ForeignKey("showtimes.id", ondelete="CASCADE"), nullable=False)

    showtime = relationship("Showtime", back_populates="seats")
    reservations = relationship("SeatReservation", back_populates="seat", cascade="all, delete-orphan")
