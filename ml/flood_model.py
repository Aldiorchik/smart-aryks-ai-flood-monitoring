import pandas as pd
import numpy as np
from pathlib import Path
import joblib
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report
import lightgbm as lgb
from model_registry.registry import register_model

"""
Smart Aryks – Flood Prediction Model

This module trains a flood risk prediction model using hydrological
sensor data generated from the Smart Aryks IoT monitoring layer.

The model predicts the probability of aryk overflow based on:

- rainfall intensity
- soil saturation
- water level
- flow velocity
- turbidity (runoff pollution indicator)
- air temperature

Algorithm:
LightGBM Gradient Boosting (efficient for tabular environmental data)

Outputs:
- trained model
- evaluation metrics
- saved model artifact
"""

DATA_PATH = Path("data/sensor_stream.csv")
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODEL_DIR / "flood_model.pkl"

FEATURE_PATH = "feature_store/features.csv"

df = pd.read_csv(FEATURE_PATH)

class FloodPredictionModel:

    def __init__(self):

        self.model = lgb.LGBMClassifier(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.9,
            colsample_bytree=0.9,
            random_state=42
        )

    def load_data(self):

        if not DATA_PATH.exists():
            raise FileNotFoundError("Sensor dataset not found")

        df = pd.read_csv(DATA_PATH)

        return df

    def create_features(self, df):

        """
        Feature engineering based on hydrological relationships.
        """

        df["rainfall_intensity"] = df["rainfall_mm"] / 5

        df["soil_saturation_index"] = df["soil_moisture"] * df["rainfall_mm"]

        df["runoff_potential"] = df["water_level_cm"] * df["soil_moisture"]

        df["pollution_index"] = df["turbidity_NTU"] * df["flow_rate_mps"]

        return df

    def create_target(self, df):

        """
        Synthetic flood risk label.

        Overflow occurs when water level and rainfall exceed thresholds.
        """

        flood_condition = (
            (df["water_level_cm"] > 95)
            | (df["rainfall_mm"] > 40)
            | ((df["soil_moisture"] > 0.7) & (df["water_level_cm"] > 80))
        )

        df["flood_risk"] = flood_condition.astype(int)

        return df

    def prepare_dataset(self, df):

        feature_cols = [
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

        X = df[feature_cols]
        y = df["flood_risk"]

        return X, y

    def train(self, X, y):

        

        X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
        )

        with mlflow.start_run():

            mlflow.log_param("model_type", "LightGBM")
            mlflow.log_param("n_estimators", 300)

            self.model.fit(X_train, y_train)

            preds = self.model.predict_proba(X_test)[:,1]

            self.auc = roc_auc_score(y_test, preds)

            mlflow.log_metric("roc_auc", self.auc)

            mlflow.sklearn.log_model(self.model, "flood_model")

            print("ROC AUC:", round(self.auc,3))

    def save_model(self):

        joblib.dump(self.model, MODEL_PATH)

        print("\nModel saved to:", MODEL_PATH)

        register_model(
        MODEL_PATH,
        {"roc_auc": self.auc}
        )


def main():

    pipeline = FloodPredictionModel()

    print("Loading sensor data...")

    df = pipeline.load_data()

    print("Generating features...")

    df = pipeline.create_features(df)

    print("Creating target labels...")

    df = pipeline.create_target(df)

    X, y = pipeline.prepare_dataset(df)

    print("Training LightGBM model...")

    pipeline.train(X, y)

    pipeline.save_model()


if __name__ == "__main__":

    main()