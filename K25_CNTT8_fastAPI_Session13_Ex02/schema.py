from pydantic import BaseModel, Field, ConfigDict
from typing import Literal


class BoardingSlotCreate(BaseModel):
    slot_number: str = Field(..., min_length=1, max_length=50)
    room_size: Literal["SMALL", "MEDIUM", "LARGE"]
    price_per_day: float = Field(..., gt=0)
    status: Literal["VACANT", "OCCUPIED"] = "VACANT"


class BoardingSlotUpdate(BaseModel):
    slot_number: str | None = Field(
        default=None,
        min_length=1,
        max_length=50
    )
    room_size: Literal["SMALL", "MEDIUM", "LARGE"] | None = None
    price_per_day: float | None = Field(default=None, gt=0)
    status: Literal["VACANT", "OCCUPIED"] | None = None


class BoardingSlotResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slot_number: str
    room_size: str
    price_per_day: float
    status: str