import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from pathlib import Path
from streamlit_autorefresh import st_autorefresh

from data.sensor_location import SENSOR_LOCATIONS

LOG_PATH = Path("logs/prediction_log.csv")

st.title("Smart Aryks Flood Risk Map")
st_autorefresh(interval=3000, key="maprefresh")

if not LOG_PATH.exists():
    st.warning("No prediction data yet")
    st.stop()

df = pd.read_csv(LOG_PATH)

latest = df.tail(len(SENSOR_LOCATIONS))

m = folium.Map(
    location=[43.2389, 76.8897],
    zoom_start=13
)

for i, sensor in enumerate(SENSOR_LOCATIONS):

    if i < len(latest):

        risk = latest.iloc[i]["risk_level"]
        prob = latest.iloc[i]["probability"]

    else:

        risk = "LOW"
        prob = 0

    if risk == "HIGH":
        color = "red"
    elif risk == "MEDIUM":
        color = "orange"
    else:
        color = "green"

    popup = f"""
    Sensor: {sensor['id']} <br>
    Location: {sensor['location']} <br>
    Flood Probability: {round(prob,2)} <br>
    Risk Level: {risk}
    """

    folium.CircleMarker(
        location=[sensor["lat"], sensor["lon"]],
        radius=10,
        popup=popup,
        color=color,
        fill=True,
        fill_opacity=0.7
    ).add_to(m)

st_folium(m, width=900)