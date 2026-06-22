import pandas as pd

from backend.services.model_loader import kmeans_model, clustering_scaler

CLUSTERING_FEATURES = [
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

CLUSTER_MAPPING = {
    0: "Moderate",
    1: "Flood-Prone",
    2: "Pollution-Prone",
    3: "Extreme-Pollution",
}


def predict_climate_profile(feature_dict):

    row = {}

    for feature in CLUSTERING_FEATURES:
        row[feature] = feature_dict.get(feature, 0)

    X = pd.DataFrame([row])

    print(X)

    X_scaled = clustering_scaler.transform(X)

    cluster = int(kmeans_model.predict(X_scaled)[0])

    print(
        "Incoming Features:",
        feature_dict.keys()
    )

    return {
        "climate_cluster": cluster,
        "climate_profile": CLUSTER_MAPPING.get(cluster, "Moderate"),
    }
