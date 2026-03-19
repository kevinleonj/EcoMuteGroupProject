"""RentalProcessing + endpoint"""
from pydantic import BaseModel, model_validator


class RentalProcessing(BaseModel):
    bike_id: int
    bike_battery: int
    user_id: int

    @model_validator(mode="after")
    def check_battery(self):
        if self.bike_battery < 20:
            raise ValueError("Bike battery too low for rental.")
        return self
    
class RentalOutcome(BaseModel):
    bike_id: int
    user_id: int
    status: str