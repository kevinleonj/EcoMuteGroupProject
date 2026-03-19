from pydantic import BaseModel, Field
from typing import Literal


BikeStatus = Literal["available", "rented", "maintenance"]



class BikeBase(BaseModel):
    model: str
    battery: float = Field(..., ge=0, le=100)
    status: BikeStatus
    station_id: int | None = None
    battery_type: str = "Standard Commuter (400-600 Wh)" 


class BikeCreate(BikeBase):
    pass


class BikeResponse(BikeBase):
    id: int


