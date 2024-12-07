from datetime import datetime

from pydantic import BaseModel, Field, FutureDatetime, PositiveInt

from app.schemas.extras import BaseFilterParams


class CreateShowtimeRequest(BaseModel):
    start_time: datetime = Field(description="Start time of the showtime")
    end_time: FutureDatetime = Field(description="End time of the showtime")
    available_seats: PositiveInt = Field(description="Number of available seats")
    total_seats: PositiveInt = Field(description="Total seats in the showtime")
    movie_id: PositiveInt = Field(description="ID of the movie for the showtime")


class ShowtimeFilterParams(BaseFilterParams):
    start_time: datetime | None = Field(None)
    end_time: datetime | None = Field(None)
    created_from: datetime | None = Field(None)
    created_to: datetime | None = Field(None)
    updated_from: datetime | None = Field(None)
    updated_to: datetime | None = Field(None)
