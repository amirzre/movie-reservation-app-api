from datetime import datetime

from pydantic import UUID4, Field

from app.schemas.extras import BaseFilterParams


class SeatFilterParams(BaseFilterParams):
    showtime_uuid: UUID4 = Field(examples=["a3b8f042-1e16-4f0a-a8f0-421e16df0a2f"])
    seat_number: str | None = Field(None, examples=["1234567890"])
    reserved: bool | None = Field(True, examples=[True])
    created_from: datetime | None = Field(None)
    created_to: datetime | None = Field(None)
    updated_from: datetime | None = Field(None)
    updated_to: datetime | None = Field(None)

    model_config = {"extra": "forbid"}
