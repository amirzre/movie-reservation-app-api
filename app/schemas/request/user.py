from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserRole
from app.schemas.extras import BaseFilterParams


class RegisterUserRequest(BaseModel):
    email: EmailStr = Field(description="Email")
    first_name: str | None = Field(max_length=50, description="Firstname")
    last_name: str | None = Field(max_length=50, description="Lastname")
    role: UserRole = Field(description="User Role")
    activated: bool = Field(description="activated")
    password: str = Field(max_length=50, description="Password")


class UpdateUserRequest(BaseModel):
    email: EmailStr | None = Field(None, description="Email")
    first_name: str | None = Field(None, max_length=50, description="Firstname")
    last_name: str | None = Field(None, max_length=50, description="Lastname")
    password: str | None = Field(None, max_length=50, description="Password")


class UserFilterParams(BaseFilterParams):
    email: EmailStr | None = Field(None)
    role: UserRole | None = Field(None)
    activated: bool = Field(True)
    created_from: datetime | None = Field(None)
    created_to: datetime | None = Field(None)
    updated_from: datetime | None = Field(None)
    updated_to: datetime | None = Field(None)

    model_config = {"extra": "forbid"}
