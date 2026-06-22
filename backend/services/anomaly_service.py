import pandas as pd

from backend.services.model_loader import isolation_forest, anomaly_scaler

ANOMALY_FEATURES = [
    "temperature_celsius",
    "humidity",
    "pressure_mb",
    "precip_mm",
    "cloud",
    "uv_index",
    "visibility_km",
    "air_quality_PM2.5",
    "air_quality_PM10",
    "air_quality_Carbon_Monoxide",
    "air_quality_Ozone",
    "air_quality_Nitrogen_dioxide",
    "air_quality_Sulphur_dioxide",
    "day_length_minutes",
    "temperature_gap",
]


def predict_anomaly(feature_dict: dict):

    X = pd.DataFrame([feature_dict], columns=ANOMALY_FEATURES)

    X_scaled = anomaly_scaler.transform(X)

    prediction = int(isolation_forest.predict(X_scaled)[0])

    status = "Normal" if prediction == 1 else "Anomaly"

    return {"anomaly_flag": prediction, "anomaly_status": status}
