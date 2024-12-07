from datetime import datetime

from pydantic import UUID4, BaseModel, Field, FutureDatetime, PositiveInt


class CreateShowtimeRequest(BaseModel):
    start_time: datetime = Field(description="Start time of the showtime")
    end_time: FutureDatetime = Field(description="End time of the showtime")
    available_seats: PositiveInt = Field(description="Number of available seats")
    total_seats: PositiveInt = Field(description="Total seats in the showtime")
    movie_id: PositiveInt = Field(description="ID of the movie for the showtime")
