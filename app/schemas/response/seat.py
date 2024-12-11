from pydantic import UUID4, BaseModel, ConfigDict, Field


class SeatResponse(BaseModel):
    uuid: UUID4 = Field(examples=["a3b8f042-1e16-4f0a-a8f0-421e16df0a2f"])
    seat_number: str = Field(examples=["1234567890"])
    reserved: bool = Field(examples=[True])

    model_config = ConfigDict(from_attributes=True)
