import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import select

from src.app.services.security import get_password_hash
from src.database import engine, async_session
from src.models import Base, Bike, User

from src.app.routers.bikes_router import router as bikes_router
from src.app.routers.user_router import router as users_router
from src.app.routers.rentals_router import router as rentals_router
from src.app.routers.admin_router import router as admin_router
from src.app.routers.auth import router as auth_router
from src.app.routers.stations import router as stations_router
from src.app.routers.predictions import router as predictions_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  —  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables ready")

    async with async_session() as session:
        has_bike = (await session.execute(select(Bike.id).limit(1))).first() is not None
        if not has_bike:
            session.add_all([
                Bike(id=1, model="EcoCruiser", battery=95, status="available", battery_type="Premium Long-Range (600-900 Wh+)"),
                Bike(id=2, model="MountainE", battery=15, status="maintenance", battery_type="Standard Commuter (400-600 Wh)"),
                Bike(id=3, model="CitySprint", battery=60, status="rented", battery_type="Small City (300-400 Wh)"),
            ])
            logger.info("Seeded 3 bikes")

        has_user = (await session.execute(select(User.id).limit(1))).first() is not None
        if not has_user:
            session.add_all([
                User(id=1, name="rider_one", email="rider@ecomute.com", hashed_password=get_password_hash("riderpass"), role="rider"),
                User(id=2, name="admin_dave", email="admin@ecomute.com", hashed_password=get_password_hash("adminpass"), role="admin"),
            ])
            logger.info("Seeded 2 users")

        await session.commit()

    logger.info("EcoMute API is ready")
    yield
    await engine.dispose()
    logger.info("EcoMute API shutting down")


app = FastAPI(title="EcoMute API", lifespan=lifespan)
app.include_router(bikes_router)
app.include_router(users_router)
app.include_router(rentals_router)
app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(stations_router)
app.include_router(predictions_router)