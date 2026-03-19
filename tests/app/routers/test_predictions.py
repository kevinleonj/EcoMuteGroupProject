import pytest
from unittest.mock import patch, MagicMock
import numpy as np


@pytest.mark.asyncio
async def test_predict_returns_estimated_minutes(async_client):
    mock_model = MagicMock()
    mock_model.predict.return_value = np.array([32.5])

    with patch("src.app.routers.predictions._model", mock_model):
        response = await async_client.post(
            "/predict",
            json={"distance_km": 10.0, "battery_level": 80},
        )

    assert response.status_code == 200
    data = response.json()
    assert "estimated_minutes" in data
    assert isinstance(data["estimated_minutes"], float)


@pytest.mark.asyncio
async def test_predict_invalid_input_returns_422(async_client):
    response = await async_client.post(
        "/predict",
        json={"distance_km": "not_a_number", "battery_level": 80},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_predict_model_not_loaded_returns_500(async_client):
    with patch("src.app.routers.predictions._model", None):
        response = await async_client.post(
            "/predict",
            json={"distance_km": 5.0, "battery_level": 50},
        )
    assert response.status_code == 500
    assert response.json()["detail"] == "Model not loaded"