import random
import time
import json
from datetime import datetime
from pathlib import Path
import pandas as pd

"""
Smart Aryks – IoT Sensor Simulation

This module simulates environmental sensors deployed in urban irrigation
channels (aryks). The simulated sensors represent the monitoring layer
described in the Smart Aryks framework:

Sensors included:
- rainfall sensor
- water level sensor
- flow rate sensor
- soil moisture sensor
- turbidity sensor (water quality)
- pH sensor (pollution indicator)
- air temperature sensor

The script generates realistic hydrological relationships between rainfall,
soil saturation, and water level in order to simulate flood risk scenarios.
"""

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = DATA_DIR / "sensor_stream.csv"


class SmartArykSensorSimulator:

    def __init__(self):

        self.base_water_level = 40
        self.base_flow = 1.2
        self.base_soil = 0.35

    def simulate_rainfall(self):

        """
        Simulate rainfall intensity (mm/hour).
        Mountain climates like Almaty show bursts of intense rainfall.
        """

        if random.random() < 0.15:
            return random.uniform(20, 60)

        return random.uniform(0, 10)

    def simulate_soil_moisture(self, rainfall):

        """
        Soil moisture increases after rainfall but slowly decreases over time.
        """

        moisture = self.base_soil + rainfall * 0.005

        moisture += random.uniform(-0.02, 0.02)

        return max(0, min(1, moisture))

    def simulate_water_level(self, rainfall, soil_moisture):

        """
        Water level increases with rainfall and saturated soil.
        """

        level = self.base_water_level

        level += rainfall * 1.2
        level += soil_moisture * 30

        level += random.uniform(-5, 5)

        return max(5, level)

    def simulate_flow_rate(self, water_level):

        """
        Flow velocity correlates with water level.
        """

        flow = self.base_flow + water_level * 0.02

        flow += random.uniform(-0.2, 0.2)

        return max(0.1, flow)

    def simulate_turbidity(self, rainfall):

        """
        Turbidity increases during rainfall due to sediment runoff.
        """

        turbidity = 5 + rainfall * 0.8

        turbidity += random.uniform(-1, 1)

        return max(0, turbidity)

    def simulate_ph(self):

        """
        Urban runoff may slightly change pH values.
        """

        ph = random.uniform(6.5, 8.2)

        return ph

    def simulate_air_temperature(self):

        """
        Air temperature influences evaporation and urban cooling.
        """

        return random.uniform(10, 35)

    def generate_reading(self):

        rainfall = self.simulate_rainfall()

        soil = self.simulate_soil_moisture(rainfall)

        water_level = self.simulate_water_level(rainfall, soil)

        flow = self.simulate_flow_rate(water_level)

        turbidity = self.simulate_turbidity(rainfall)

        ph = self.simulate_ph()

        temperature = self.simulate_air_temperature()

        timestamp = datetime.utcnow().isoformat()

        return {
            "timestamp": timestamp,
            "rainfall_mm": rainfall,
            "soil_moisture": soil,
            "water_level_cm": water_level,
            "flow_rate_mps": flow,
            "turbidity_NTU": turbidity,
            "ph": ph,
            "air_temperature_c": temperature
        }


def save_reading(data):

    df = pd.DataFrame([data])

    file_exists = OUTPUT_FILE.exists()

    df.to_csv(
        OUTPUT_FILE,
        mode="a",
        header=not file_exists,
        index=False
    )


def simulate_stream():

    simulator = SmartArykSensorSimulator()

    print("Starting Smart Aryks sensor stream...\n")

    while True:

        reading = simulator.generate_reading()

        save_reading(reading)

        print(json.dumps(reading, indent=2))

        time.sleep(5)


if __name__ == "__main__":

    simulate_stream()