from datetime import datetime

from pydantic import Field

from app.schemas.extras import BaseFilterParams


class SeatFilterParams(BaseFilterParams):
    seat_number: str | None = Field(None)
    reserved: bool | None = Field(True)
    created_from: datetime | None = Field(None)
    created_to: datetime | None = Field(None)
    updated_from: datetime | None = Field(None)
    updated_to: datetime | None = Field(None)

    model_config = {"extra": "forbid"}
