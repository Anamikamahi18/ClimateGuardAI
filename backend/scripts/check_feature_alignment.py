import joblib

from backend.services.weather_service import (
    get_coordinates,
    get_weather_data,
    get_air_quality_data,
)

from backend.preprocessing.inference_pipeline import build_rainfall_features

# ====================================
# LOAD TRAINING FEATURES
# ====================================

training_features = joblib.load("models/rainfall_feature_names.pkl")

# ====================================
# GENERATE LIVE FEATURES
# ====================================

location = get_coordinates("Kochi")

weather = get_weather_data(location["latitude"], location["longitude"])

air = get_air_quality_data(location["latitude"], location["longitude"])

live_features = build_rainfall_features(weather, air, location)

live_feature_names = list(live_features.keys())

# ====================================
# COMPARE
# ====================================

missing = set(training_features) - set(live_feature_names)

extra = set(live_feature_names) - set(training_features)

print("Missing:", len(missing))
print(missing)

print()

print("Extra:", len(extra))
print(extra)
