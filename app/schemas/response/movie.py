from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict, Field


class MovieResponse(BaseModel):
    uuid: UUID4 = Field(examples=["a3b8f042-1e16-4f0a-a8f0-421e16df0a2f"])
    title: str = Field(examples=["Movie Title"])
    description: str = Field(examples=["Movie Description"])
    genre: str = Field(examples=["Action"])
    release_date: datetime = Field(examples=["2024-09-17 04:18:12.176290"])
    activated: bool = Field(examples=[True])

    model_config = ConfigDict(from_attributes=True)
