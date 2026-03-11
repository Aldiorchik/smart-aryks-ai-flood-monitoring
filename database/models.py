from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

Base = declarative_base()


class SensorReading(Base):

    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True)

    rainfall = Column(Float)
    soil_moisture = Column(Float)
    water_level = Column(Float)
    flow_rate = Column(Float)

    timestamp = Column(DateTime, default=datetime.utcnow)


class FloodPrediction(Base):

    __tablename__ = "flood_predictions"

    id = Column(Integer, primary_key=True)

    probability = Column(Float)
    risk_level = Column(String)

    timestamp = Column(DateTime, default=datetime.utcnow)


class CitizenReport(Base):

    __tablename__ = "citizen_reports"

    id = Column(Integer, primary_key=True)

    image_path = Column(String)
    label = Column(String)
    probability = Column(Float)

    timestamp = Column(DateTime, default=datetime.utcnow)

print("Database initialized successfully")