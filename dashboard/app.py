import pandas as pd
import joblib
from pathlib import Path
from datetime import datetime
import logging

"""
Smart Aryks – Prediction Service

This service performs real-time flood prediction using
sensor data from the Smart Aryks monitoring network.

Responsibilities:

1. Load trained ML model
2. Validate incoming sensor data
3. Generate features
4. Predict flood risk
5. Produce alerts
6. Log prediction events
"""

MODEL_PATH = Path("models/flood_model.pkl")
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "prediction_log.csv"


class FloodPredictor:

    def __init__(self):

        if not MODEL_PATH.exists():
            raise FileNotFoundError("Model file not found")

        self.model = joblib.load(MODEL_PATH)

    def feature_engineering(self, df):

        """
        Create same engineered features used during training
        """

        df["rainfall_intensity"] = df["rainfall_mm"] / 5

        df["soil_saturation_index"] = df["soil_moisture"] * df["rainfall_mm"]

        df["runoff_potential"] = df["water_level_cm"] * df["soil_moisture"]

        df["pollution_index"] = df["turbidity_NTU"] * df["flow_rate_mps"]

        return df

    def predict(self, data):

        df = pd.DataFrame([data])

        df = self.feature_engineering(df)

        features = [
            "rainfall_mm",
            "soil_moisture",
            "water_level_cm",
            "flow_rate_mps",
            "turbidity_NTU",
            "ph",
            "air_temperature_c",
            "rainfall_intensity",
            "soil_saturation_index",
            "runoff_potential",
            "pollution_index"
        ]

        X = df[features]

        probability = self.model.predict_proba(X)[0][1]

        prediction = int(probability > 0.5)

        return prediction, probability

    def risk_level(self, probability):

        """
        Convert probability into interpretable risk category
        """

        if probability < 0.3:
            return "LOW"

        if probability < 0.6:
            return "MEDIUM"

        return "HIGH"

    def generate_alert(self, risk_level):

        if risk_level == "HIGH":
            return "Flood risk detected – immediate inspection required"

        if risk_level == "MEDIUM":
            return "Potential overflow conditions developing"

        return "System operating normally"

    def log_prediction(self, sensor_data, prediction, probability, risk):

        record = {
            "timestamp": datetime.utcnow().isoformat(),
            **sensor_data,
            "prediction": prediction,
            "probability": probability,
            "risk_level": risk
        }

        df = pd.DataFrame([record])

        file_exists = LOG_FILE.exists()

        df.to_csv(
            LOG_FILE,
            mode="a",
            header=not file_exists,
            index=False
        )

    def process(self, sensor_data):

        prediction, probability = self.predict(sensor_data)

        risk = self.risk_level(probability)

        alert = self.generate_alert(risk)

        self.log_prediction(sensor_data, prediction, probability, risk)

        return {
            "prediction": prediction,
            "probability": round(probability, 3),
            "risk_level": risk,
            "alert": alert
        }


def demo():

    """
    Example test request simulating sensor input
    """

    predictor = FloodPredictor()

    sample_data = {

        "rainfall_mm": 35,
        "soil_moisture": 0.75,
        "water_level_cm": 95,
        "flow_rate_mps": 2.1,
        "turbidity_NTU": 30,
        "ph": 7.1,
        "air_temperature_c": 22
    }

    result = predictor.process(sample_data)

    print("\nPrediction result\n")
    print(result)


if __name__ == "__main__":

    demo()