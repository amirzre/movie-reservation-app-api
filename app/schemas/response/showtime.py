from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, FutureDatetime, PositiveInt

from .movie import MovieResponse


class ShowtimeResponse(BaseModel):
    id: PositiveInt = Field(examples=[1])
    start_time: datetime = Field(examples=["2024-09-17T04:18:12.176290"])
    end_time: FutureDatetime = Field(examples=["2024-09-17T06:18:12.176290"])
    available_seats: PositiveInt = Field(examples=[20])
    total_seats: PositiveInt = Field(examples=[100])
    movie: MovieResponse

    model_config = ConfigDict(from_attributes=True)
