# Smart Aryks – AI Urban Flood Monitoring System

Smart Aryks is an AI-powered urban flood monitoring platform designed to predict irrigation canal overflow using IoT sensors, machine learning, and citizen reports.

The goal of the project is to demonstrate a **production-style ML system architecture**, including data pipelines, model training, experiment tracking, model registry, APIs, monitoring dashboards, and automated retraining.

This project focuses on **ML engineering and system design**, not just model training.

---

# System Architecture

```mermaid
flowchart TD

    A[IoT Sensors Water Level Rainfall] --> B[Sensor Stream]

    B --> C[Feature Store]

    C --> D[ML Training Pipeline]

    D --> E[MLflow Experiment Tracking]

    E --> F[Model Registry]

    F --> G[Prediction API FastAPI]

    G --> H[PostgreSQL Database]

    H --> I[Monitoring Dashboard Streamlit]

    H --> J[Flood Risk Map GIS Visualization]

    K[Citizen Reports Image Upload] --> L[Computer Vision Model]

    L --> H

    M[Retraining Scheduler] --> D

## Key Features

### IoT Sensor Simulation

The system simulates environmental sensors monitoring urban irrigation canals.

Sensors generate data for:

- rainfall intensity
- water level
- water flow velocity
- soil moisture
- turbidity (water quality)
- air temperature

This data is used to simulate a real-world monitoring environment.

---

### Flood Prediction Model

A machine learning model predicts flood risk based on environmental sensor data.

Model characteristics:

- algorithm: LightGBM
- features: rainfall, soil moisture, water level, flow rate, turbidity
- evaluation metric: ROC AUC

Feature engineering includes:

- rainfall intensity
- soil saturation index
- runoff potential
- pollution index

---

### Feature Store

The project includes a centralized feature generation pipeline.

The feature store ensures that the same features are used during both training and inference, preventing training-serving skew.

---

### Experiment Tracking

Model training experiments are tracked using **MLflow**.

MLflow allows tracking:

- experiment runs
- model parameters
- evaluation metrics
- trained model artifacts

This enables easy comparison between different model versions.

---

### Model Registry

A lightweight model registry stores information about trained models:

- model location
- evaluation metrics
- training timestamp

This allows version control for machine learning models.

---

### Prediction API

A FastAPI service exposes the trained model as an inference API.

Available endpoints:
## Key Features

### IoT Sensor Simulation

The system simulates environmental sensors monitoring urban irrigation canals.

Sensors generate data for:

- rainfall intensity
- water level
- water flow velocity
- soil moisture
- turbidity (water quality)
- air temperature

This data is used to simulate a real-world monitoring environment.

---

### Flood Prediction Model

A machine learning model predicts flood risk based on environmental sensor data.

Model characteristics:

- algorithm: LightGBM
- features: rainfall, soil moisture, water level, flow rate, turbidity
- evaluation metric: ROC AUC

Feature engineering includes:

- rainfall intensity
- soil saturation index
- runoff potential
- pollution index

---

### Feature Store

The project includes a centralized feature generation pipeline.

The feature store ensures that the same features are used during both training and inference, preventing training-serving skew.

---

### Experiment Tracking

Model training experiments are tracked using **MLflow**.

MLflow allows tracking:

- experiment runs
- model parameters
- evaluation metrics
- trained model artifacts

This enables easy comparison between different model versions.

---

### Model Registry

A lightweight model registry stores information about trained models:

- model location
- evaluation metrics
- training timestamp

This allows version control for machine learning models.

---

### Prediction API

A FastAPI service exposes the trained model as an inference API.

Available endpoints:
POST /predict
GET /health
GET /latest


The API returns:

- flood probability
- risk level
- alert message

---

### PostgreSQL Event Storage

The system can store events in PostgreSQL, including:

- sensor readings
- flood predictions
- citizen reports

This enables monitoring and analytics.

---

### Monitoring Dashboard

A Streamlit dashboard provides visualization for:

- hydrological sensor data
- flood prediction statistics
- recent system activity
- system health metrics

---

### GIS Flood Risk Map

An interactive GIS map displays flood risk across monitored locations.

Risk levels are visualized as:

- green – low risk
- orange – medium risk
- red – high risk

The map automatically refreshes to simulate real-time monitoring.

---

### Citizen Reporting System

Citizens can upload images of blocked irrigation canals.

The system processes images using a computer vision model to detect potential blockages.

Pipeline:
Citizen photo → Computer vision model → Blockage detection → Database → Dashboard alert


---

### Automated Retraining Pipeline

A scheduler automatically retrains the flood prediction model using new sensor data.

Pipeline:
sensor data → feature store → training → model registry → deployment


This simulates a production MLOps workflow.

---

## Project Structure
smart-aryks

ml/
    flood_model.py

sensors/
    simulate_sensor.py

api/
    main.py
    predict_service.py

dashboard/
    app.py
    map_dashboard.py

citizen_reports/
    api.py
    detect_blockage.py

feature_store/
    feature_pipeline.py

model_registry/
    registry.py

pipeline/
    retrain_pipeline.py

database/
    models.py
    init_db.py


---

## Running the System

### Start sensor simulation

python sensors/simulate_sensor.py


### Train the model

python -m ml.flood_model

### Start prediction API
uvicorn api.main:app --reload

### Start monitoring dashboard
streamlit run dashboard/app.py

### Start flood risk map
streamlit run dashboard/map_dashboard.py

### Start MLflow experiment tracking
mlflow ui

Open in browser:
http://127.0.0.1:5000


---

## Tech Stack

- Python  
- FastAPI  
- LightGBM  
- Streamlit  
- PostgreSQL  
- MLflow  
- SQLAlchemy  
- Pandas  
- Scikit-learn  

---

## Engineering Focus

This project focuses on machine learning system design, including:

- production-style ML pipelines
- experiment tracking
- model versioning
- automated retraining
- monitoring and observability
- modular architecture

---

## Possible Extensions

Future improvements could include:

- distributed training
- online learning models
- CI/CD pipelines for ML
- Kubernetes deployment
- real-time streaming with Kafka