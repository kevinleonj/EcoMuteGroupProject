import logging
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s")
logger = logging.getLogger(__name__)


def train_and_save(output_path: str = "src/ml/trip_predictor.joblib") -> None:
    n_samples = 1000
    distances = np.random.uniform(1, 20, n_samples)
    battery_levels = np.random.uniform(10, 100, n_samples)
    minutes = (3 * distances) + (100 - battery_levels) + np.random.normal(0, 2, n_samples)

    X = pd.DataFrame({"distance": distances, "battery": battery_levels})
    model = LinearRegression()
    model.fit(X, minutes)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_path)
    logger.info("Model trained and saved to '%s'", output_path)


if __name__ == "__main__":
    train_and_save()