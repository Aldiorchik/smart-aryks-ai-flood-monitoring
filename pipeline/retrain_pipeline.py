import schedule
import time
import subprocess

"""
Smart Aryks Retraining Pipeline

Automatically retrains the flood prediction model
when new sensor data is available.
"""

def retrain_model():

    print("\nStarting automated retraining pipeline...\n")

    subprocess.run(["python", "-m", "feature_store.feature_pipeline"])

    subprocess.run(["python", "-m", "ml.flood_model"])

    print("\nRetraining completed\n")


schedule.every(1).hours.do(retrain_model)


print("Smart Aryks retraining scheduler started")


while True:

    schedule.run_pending()

    time.sleep(60)