from pydantic import UUID4, BaseModel, ConfigDict, Field


class UserResponse(BaseModel):
    uuid: UUID4 = Field(examples=["a3b8f042-1e16-4f0a-a8f0-421e16df0a2f"])
    email: str = Field(examples=["johndoe@example.com"])
    first_name: str = Field(examples=["john"])
    last_name: str = Field(examples=["doe"])
    role: str = Field(examples=["USER"])
    activated: bool = Field(examples=[True])

    model_config = ConfigDict(from_attributes=True)
