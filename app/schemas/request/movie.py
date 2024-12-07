from datetime import datetime

from pydantic import BaseModel, Field, FutureDatetime

from app.schemas.extras import BaseFilterParams


class CreateMovieRequest(BaseModel):
    title: str = Field(max_length=255, description="Movie Title")
    description: str | None = Field(max_length=1000, description="Movie description")
    genre: str = Field(max_length=50, description="Movie genre")
    release_date: FutureDatetime = Field(description="Movie release date")
    activated: bool | None = Field(default=True, description="Activated")


class UpdateMovieRequest(BaseModel):
    title: str | None = Field(None, max_length=255, description="Movie Title")
    description: str | None = Field(None, max_length=1000, description="Movie description")
    genre: str | None = Field(None, max_length=50, description="Movie genre")
    release_date: FutureDatetime | None = Field(None, description="Movie release date")
    activated: bool | None = Field(None, description="Activated")


class MovieFilterParams(BaseFilterParams):
    title: str | None = Field(None)
    genre: str | None = Field(None)
    release_date: datetime | None = Field(None)
    activated: bool | None = Field(True)
    created_from: datetime | None = Field(None)
    created_to: datetime | None = Field(None)
    updated_from: datetime | None = Field(None)
    updated_to: datetime | None = Field(None)

    model_config = {"extra": "forbid"}
