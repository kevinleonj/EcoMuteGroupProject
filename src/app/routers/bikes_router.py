# lab 4 add Depends, Annotated - ex1
from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List, Optional, Annotated
from src.app.models.bikes import BikeCreate, BikeResponse, BikeStatus
# lab 5
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from src.database import get_db
from src.models import Bike
# lab 9
from src.app.logger import logger

# lab 4 - dependency function - ex1
router = APIRouter(
    prefix="/bikes",
    tags=["bikes"],
)

# Annotated dependency alias (lab 4 - commented, kept for reference)
# BikesDep = Annotated[BikesDataSource, Depends(get_bikes_datasource)]


@router.get("/", response_model=list[BikeResponse], response_model_by_alias=False)
async def get_bikes(
    status: BikeStatus | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    logger.info("Fetching all bikes")
    result = await db.execute(select(Bike))
    bikes = result.scalars().all()

    if status is not None:
        bikes = [bike for bike in bikes if bike.status == status]

    if not bikes:
        logger.warning("No bikes found in database")

    return bikes


@router.get("/{bike_id}", response_model=BikeResponse, response_model_by_alias=False)
async def get_bike(bike_id: int, db: AsyncSession = Depends(get_db)):
    logger.info("Fetching bike id=%d", bike_id)
    bike = await db.get(Bike, bike_id)
    if bike is None:
        logger.warning("Bike id=%d not found", bike_id)
        raise HTTPException(status_code=404, detail="Bike not found")
    return bike


@router.post("/", response_model=BikeResponse, response_model_by_alias=False,
             status_code=status.HTTP_201_CREATED)
async def create_bike(bike: BikeCreate, db: AsyncSession = Depends(get_db)):
    logger.info("Creating new bike: %s", bike.model)
    new_bike = Bike(**bike.model_dump())
    db.add(new_bike)
    await db.commit()
    await db.refresh(new_bike)
    return new_bike


@router.put("/{bike_id}", response_model=BikeResponse, response_model_by_alias=False)
async def update_bike(bike_id: int, bike: BikeCreate, db: AsyncSession = Depends(get_db)):
    logger.info("Updating bike id=%d", bike_id)
    existing = await db.get(Bike, bike_id)
    if existing is None:
        logger.warning("Update failed — bike id=%d not found", bike_id)
        raise HTTPException(status_code=404, detail="Bike not found")
    for key, value in bike.model_dump().items():
        setattr(existing, key, value)
    await db.commit()
    await db