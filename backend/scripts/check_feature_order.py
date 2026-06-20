import joblib

from backend.services.weather_service import (
    get_coordinates,
    get_weather_data,
    get_air_quality_data,
)

from backend.preprocessing.inference_pipeline import build_rainfall_features

training_features = joblib.load("models/rainfall_feature_names.pkl")

location = get_coordinates("Kochi")

weather = get_weather_data(location["latitude"], location["longitude"])

air = get_air_quality_data(location["latitude"], location["longitude"])

features = build_rainfall_features(weather, air, location)

live_features = list(features.keys())

print(training_features[:20])

print()

print(live_features[:20])

print()

print(training_features == live_features)
