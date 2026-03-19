"""RentalProcessing + endpoint"""
from fastapi import APIRouter, Depends, HTTPException
#lab 5
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.app.models.rentals import RentalProcessing, RentalOutcome
#lab5 
from src.database import get_db
from src.models import Bike, Rental

#change status if bike rented + lab4 - ex 3
#from src.app.data.bikes_data_source import BikesDataSource

router = APIRouter(prefix="/rentals", tags=["rentals"])

#change status if bike rented
#def get_bikes_data_source():
#    return BikesDataSource()

@router.post("/", response_model=RentalOutcome)
async def create_rental(
    rental: RentalProcessing,
    db: AsyncSession = Depends(get_db),
):
     # Find bike in database
    stmt = select(Bike).where(Bike.id == rental.bike_id)
    result = await db.execute(stmt)
    bike = result.scalar_one_or_none()

    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")

    # Create rental record
    new_rental = Rental(
        bike_id=rental.bike_id,
        user_id=rental.user_id,
    )

    db.add(new_rental)

    # Update bike status
    bike.status = "rented"

    await db.commit()
    await db.refresh(new_rental)

    return RentalOutcome(
        bike_id=rental.bike_id,
        user_id=rental.user_id,
        status=bike.status,
    )


#def create_rental(rental: RentalProcessing,
    #lab 4 + change bike status
    #bikes: BikesDataSource = Depends(get_bikes_data_source)
#):
    #bike = bikes.get_bike(rental.bike_id)

    #if not bike:
    #    raise HTTPException(status_code=404, detail="Bikes not found")
    
    #bike["status"]= "rented"

    #return {"message": "Rental processed successfully"}
