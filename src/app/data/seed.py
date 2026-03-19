from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Bike, User
from src.app.services.security import get_password_hash


INITIAL_BIKES = [
    {"model": "EcoCruiser", "status": "available", "battery": 95},
    {"model": "MountainE", "status": "maintenance", "battery": 15},
    {"model": "CitySprint", "status": "rented", "battery": 60},
]

INITIAL_USERS = [
    {"name": "rider_one", "email": "rider_one@eco.com", "role": "rider"},
    {"name": "admin_dave", "email": "admin@eco.com", "role": "admin"},
]


async def seed_data(db: AsyncSession):
    print("🌱 Checking if database needs seeding...")

    result = await db.execute(select(Bike).limit(1))
    first_bike = result.scalar_one_or_none()

    if first_bike:
        print("✅ Database already contains data. Skipping seed.")
        return

    print("🚀 Seeding database with initial mock data...")

    # Add bikes
    for bike_data in INITIAL_BIKES:
        new_bike = Bike(**bike_data)
        db.add(new_bike)

    # Add users (with hashed passwords - LAB5)
    for user_data in INITIAL_USERS:
        new_user = User(
            name=user_data["name"],
            email=user_data["email"],
            hashed_password=get_password_hash("test123"),
            role=user_data["role"]
        )
        db.add(new_user)

    await db.commit()
    print("🎉 Seeding complete!")