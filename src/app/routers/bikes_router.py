#lab 4 add Depends, Annotated - ex1
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional, Annotated
from src.app.models.bikes import BikeCreate, BikeResponse, BikeStatus
#lab 5 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from src.database import get_db
from src.models import Bike

#lab 4 - dependency function - ex1
router = APIRouter(
    prefix="/bikes",
    tags=["bikes"],
    #dependencies=[Depends(get_bikedatasource)]
)

#bikes = BikesDataSource() - router directly creates the datasource

# Annotated dependency alias
#BikesDep = Annotated[BikesDataSource, Depends(get_bikes_datasource)]


@router.get("/", response_model=List[BikeResponse])
async def read_bikes(
    db: AsyncSession = Depends(get_db),
    status: Optional[BikeStatus] = Query(default=None)
):
    stmt = select(Bike)

    if status:
        stmt = stmt.where(Bike.status == status)

    result = await db.execute(stmt)
    bikes = result.scalars().all()

    return bikes 

@router.get("/{bike_id}", response_model=BikeResponse)
async def read_bike(
    bike_id: int,
    db: AsyncSession = Depends(get_db)   
    ):
    stmt = select(Bike).where(Bike.id == bike_id)
    result = await db.execute(stmt)
    bike = result.scalar_one_or_none()

    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")

    return bike

@router.post("/", response_model=BikeResponse)
async def create_bike(
    bike: BikeCreate,
    db: AsyncSession = Depends(get_db)
):
    new_bike = Bike(**bike.model_dump())
    db.add(new_bike)

    await db.commit()
    await db.refresh(new_bike)

    return new_bike

@router.put("/{bike_id}", response_model=BikeResponse)
async def update_bike(
    bike_id: int,
    bike: BikeCreate,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Bike).where(Bike.id == bike_id)
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()

    if not existing:
        raise HTTPException(status_code=404, detail="Bike not found")

    for key, value in bike.model_dump().items():
        setattr(existing, key, value)

    await db.commit()
    await db.refresh(existing)

    return existing


@router.delete("/{bike_id}")
async def delete_bike(
    bike_id: int,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Bike).where(Bike.id == bike_id)
    result = await db.execute(stmt)
    bike = result.scalar_one_or_none()

    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")

    await db.delete(bike)
    await db.commit()

    return {"deleted": True}
