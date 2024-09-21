from pydantic import BaseModel, Field, FutureDatetime


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
