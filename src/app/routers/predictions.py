import asyncio
import logging
import os

import joblib
import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(tags=["ML Prediction"])

_model = None

MODEL_PATH = "src/ml/trip_predictor.joblib"
if os.path.exists(MODEL_PATH):
    _model = joblib.load(MODEL_PATH)
    logger.info("ML model loaded from '%s'", MODEL_PATH)
else:
    logger.warning("Model not found at '%s'. Run src/ml/train.py first.", MODEL_PATH)


class TripInput(BaseModel):
    distance_km: float
    battery_level: int


def _run_prediction(distance_km: float, battery_level: int) -> float:
    features = pd.DataFrame({"distance": [distance_km], "battery": [battery_level]})
    return float(_model.predict(features)[0])


@router.post("/predict")
async def predict_duration(data: TripInput):
    if _model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    logger.info("Prediction request: %.1f km, %d%% battery", data.distance_km, data.battery_level)
    prediction = await asyncio.to_thread(_run_prediction, data.distance_km, data.battery_level)
    logger.info("Prediction result: %.1f minutes", prediction)
    return {"estimated_minutes": round(prediction, 1)}