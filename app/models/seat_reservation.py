from uuid import uuid4

from pydantic import UUID4
from sqlalchemy import UUID, BigInteger, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base
from core.db.mixins import TimestampMixin


class SeatReservation(Base, TimestampMixin):
    __tablename__ = "seat_reservations"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    uuid: Mapped[UUID4] = mapped_column(UUID, unique=True, index=True, default=uuid4)
    reservation_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("reservations.id", ondelete="CASCADE"), nullable=False
    )
    seat_id: Mapped[int] = mapped_column(Integer, ForeignKey("seats.id", ondelete="CASCADE"), nullable=False)

    reservation = relationship("Reservation", back_populates="seats")
    seat = relationship("Seat", back_populates="reservations")
