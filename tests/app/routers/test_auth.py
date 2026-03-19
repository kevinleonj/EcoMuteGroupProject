import pytest

@pytest.mark.asyncio
async def test_stations_requires_auth(async_client):
    response = await async_client.post("/stations/")
    assert response.status_code == 401

import pytest
from src.models import User
from src.app.services.security import get_password_hash


@pytest.mark.asyncio
async def test_stations_forbidden_for_rider(async_client, db_session):
    # Arrange: create rider user
    rider = User(
        name="Test Rider",
        email="rider@test.com",
        hashed_password=get_password_hash("test123"),
        role="rider"
    )
    db_session.add(rider)
    await db_session.commit()

    # Login to get token
    login_response = await async_client.post(
        "/token",
        data={"username": "rider@test.com", "password": "test123"}
    )
    token = login_response.json()["access_token"]

    # Call protected endpoint with rider token
    response = await async_client.post(
        "/stations/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403

@pytest.mark.asyncio
async def test_stations_allowed_for_admin(async_client, db_session):
    # Arrange: create admin user
    admin = User(
        name="Admin User",
        email="admin@test.com",
        hashed_password=get_password_hash("test123"),
        role="admin"
    )
    db_session.add(admin)
    await db_session.commit()

    # Login to get token
    login_response = await async_client.post(
        "/token",
        data={"username": "admin@test.com", "password": "test123"}
    )
    token = login_response.json()["access_token"]

    # Call protected endpoint with admin token
    response = await async_client.post(
        "/stations/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200