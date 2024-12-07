from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict, Field, PositiveInt

from app.schemas.response import MovieResponse


class ShowtimeResponse(BaseModel):
    id: PositiveInt = Field(examples=[1])
    uuid: UUID4 = Field(examples=["a3b8f042-1e16-4f0a-a8f0-421e16df0a2f"])
    start_time: datetime = Field(examples=["2024-09-17T04:18:12.176290"])
    end_time: datetime = Field(examples=["2024-09-17T06:18:12.176290"])
    available_seats: PositiveInt = Field(examples=[20])
    total_seats: PositiveInt = Field(examples=[100])
    movie: MovieResponse | None = Field(None, description="Related Movie")

    model_config = ConfigDict(from_attributes=True)
