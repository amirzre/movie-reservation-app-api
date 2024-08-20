from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserRole


class RegisterUserRequest(BaseModel):
    email: EmailStr = Field(description="Email")
    first_name: str | None = Field(max_length=50, description="Firstname")
    last_name: str | None = Field(max_length=50, description="Lastname")
    role: UserRole | None = Field(description="User Role")
    activated: bool = Field(description="activated")
    password: str = Field(max_length=50, description="Password")


class UpdateUserRequest(BaseModel):
    email: EmailStr | None = Field(None, description="Email")
    first_name: str | None = Field(None, max_length=50, description="Firstname")
    last_name: str | None = Field(None, max_length=50, description="Lastname")
    password: str | None = Field(None, max_length=50, description="Password")
