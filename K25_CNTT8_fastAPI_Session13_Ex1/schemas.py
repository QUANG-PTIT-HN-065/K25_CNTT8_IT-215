from pydantic import BaseModel, Field, ConfigDict
from typing import Literal


class MenuItemCreate(BaseModel):
    dish_code: str = Field(..., min_length=1, max_length=50)
    dish_name: str = Field(..., min_length=1, max_length=100)
    calorie_count: int = Field(..., gt=0)
    price: float = Field(..., gt=0)
    status: Literal["AVAILABLE", "OUT_OF_STOCK"] = "AVAILABLE"


class MenuItemUpdate(BaseModel):
    dish_code: str | None = Field(None, min_length=1, max_length=50)
    dish_name: str | None = Field(None, min_length=1, max_length=100)
    calorie_count: int | None = Field(None, gt=0)
    price: float | None = Field(None, gt=0)
    status: Literal["AVAILABLE", "OUT_OF_STOCK"] | None = None


class MenuItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    dish_code: str
    dish_name: str
    calorie_count: int
    price: float
    status: str