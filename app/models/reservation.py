from datetime import datetime
from enum import auto
from uuid import uuid4

from pydantic import UUID4
from sqlalchemy import UUID, BigInteger, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base
from core.db.mixins import TimestampMixin
from core.enum import StrEnum


class ReservationStatus(StrEnum):
    PENDING = auto()
    CONFIRMED = auto()
    CANCELED = auto()


class Reservation(Base, TimestampMixin):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    uuid: Mapped[UUID4] = mapped_column(UUID, unique=True, index=True, default=uuid4)
    status: Mapped[ReservationStatus] = mapped_column(
        Enum(ReservationStatus), default=ReservationStatus.PENDING, nullable=False
    )
    reserved: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    showtime_id: Mapped[int] = mapped_column(Integer, ForeignKey("showtimes.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="reservations")
    showtime = relationship("Showtime", back_populates="reservations")
