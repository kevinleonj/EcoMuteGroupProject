import pytest
from src.models import Bike

@pytest.mark.asyncio
async def test_get_single_bike_by_id(async_client, db_session):
    # Arrange: insert one bike
    bike = Bike(model="SingleBike", battery=90, status="available")
    db_session.add(bike)
    await db_session.commit()

    # Act: fetch by ID
    response = await async_client.get(f"/bikes/{bike.id}")

    # Assert
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == bike.id
    assert data["model"] == "SingleBike"
    assert data["battery"] == 90
    assert data["status"] == "available"

@pytest.mark.asyncio
async def test_get_bikes_returns_one(async_client, db_session):
    # Arrange: insert one bike into test DB
    bike = Bike(model="TestBike", battery=100, status="available")
    db_session.add(bike)
    await db_session.commit()

    # Act: call API
    response = await async_client.get("/bikes/")
    
    # Assert
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["model"] == "TestBike"
    assert data[0]["battery"] == 100
    assert data[0]["status"] == "available"

#other tests Exercice 5

@pytest.mark.asyncio
async def test_create_bike(async_client):
    payload = {
        "model": "NewBike",
        "battery": 80,
        "status": "available"
    }

    response = await async_client.post("/bikes/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["model"] == "NewBike"
    assert data["battery"] == 80


@pytest.mark.asyncio
async def test_get_nonexistent_bike(async_client):
    response = await async_client.get("/bikes/999")

    assert response.status_code == 404