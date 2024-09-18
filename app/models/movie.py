from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, BigInteger, Boolean, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base
from core.db.mixins import TimestampMixin


class Movie(Base, TimestampMixin):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column(UUID, unique=True, index=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    poster: Mapped[str] = mapped_column(String, nullable=True)
    genre: Mapped[str] = mapped_column(String(50), nullable=False)
    release_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    activated: Mapped[bool] = mapped_column(Boolean, default=True)
