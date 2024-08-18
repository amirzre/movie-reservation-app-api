from enum import auto
from uuid import uuid4

from sqlalchemy import UUID, BigInteger, Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base
from core.db.mixins import TimestampMixin
from core.enum import StrEnum


class UserRole(StrEnum):
    ADMIN = auto()
    USER = auto()


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column(UUID, unique=True, index=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[Enum] = mapped_column(Enum(UserRole), default=UserRole.USER, nullable=False)
    activated: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
