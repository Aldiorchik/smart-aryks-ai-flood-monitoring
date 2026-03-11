import pandas as pd
from pathlib import Path

"""
Smart Aryks Feature Store

Centralized feature generation used by both:
- training pipeline
- prediction service
"""

DATA_PATH = Path("data/sensor_stream.csv")
FEATURE_PATH = Path("feature_store/features.csv")


def generate_features():

    df = pd.read_csv(DATA_PATH)

    df["rainfall_intensity"] = df["rainfall_mm"] / 5

    df["soil_saturation_index"] = df["soil_moisture"] * df["rainfall_mm"]

    df["runoff_potential"] = df["water_level_cm"] * df["soil_moisture"]

    df["pollution_index"] = df["turbidity_NTU"] * df["flow_rate_mps"]

    FEATURE_PATH.parent.mkdir(exist_ok=True)

    df.to_csv(FEATURE_PATH, index=False)

    print("Features stored in feature_store")


if __name__ == "__main__":

    generate_features()