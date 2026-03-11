import streamlit as st
import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/sensor_stream.csv")
LOG_PATH = Path("logs/prediction_log.csv")

st.set_page_config(
    page_title="Smart Aryks Monitoring",
    layout="wide"
)

st.title("Smart Aryks Urban Water Monitoring Dashboard")

def load_sensor_data():

    if not DATA_PATH.exists():
        return pd.DataFrame()

    return pd.read_csv(DATA_PATH)


def load_predictions():

    if not LOG_PATH.exists():
        return pd.DataFrame()

    return pd.read_csv(LOG_PATH)


sensor_df = load_sensor_data()
pred_df = load_predictions()

if sensor_df.empty:

    st.warning("No sensor data available yet. Run sensor simulator.")

    st.stop()

st.sidebar.header("System Overview")

st.sidebar.metric(
    "Total Sensor Readings",
    len(sensor_df)
)

if not pred_df.empty:

    high_risk = len(pred_df[pred_df["risk_level"] == "HIGH"])

    st.sidebar.metric(
        "High Risk Events",
        high_risk
    )

st.header("Hydrological Monitoring")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Water Level")

    st.line_chart(sensor_df["water_level_cm"])

with col2:

    st.subheader("Rainfall Intensity")

    st.line_chart(sensor_df["rainfall_mm"])

col3, col4 = st.columns(2)

with col3:

    st.subheader("Soil Moisture")

    st.line_chart(sensor_df["soil_moisture"])

with col4:

    st.subheader("Flow Velocity")

    st.line_chart(sensor_df["flow_rate_mps"])

st.header("Water Quality")

col5, col6 = st.columns(2)

with col5:

    st.subheader("Turbidity")

    st.line_chart(sensor_df["turbidity_NTU"])

with col6:

    st.subheader("pH Levels")

    st.line_chart(sensor_df["ph"])

st.header("Recent Sensor Data")

st.dataframe(sensor_df.tail(20))

if not pred_df.empty:

    st.header("Flood Prediction Alerts")

    latest = pred_df.tail(10)

    st.dataframe(latest)

    st.subheader("Risk Distribution")

    risk_counts = pred_df["risk_level"].value_counts()

    st.bar_chart(risk_counts)

    st.subheader("Flood Probability Over Time")

    st.line_chart(pred_df["probability"])

st.header("System Status")

if not pred_df.empty:

    latest_risk = pred_df.iloc[-1]["risk_level"]

    if latest_risk == "HIGH":
        st.error("High flood risk detected")

    elif latest_risk == "MEDIUM":
        st.warning("Moderate flood risk developing")

    else:
        st.success("System operating normally")

else:

    st.info("Prediction system not active yet")