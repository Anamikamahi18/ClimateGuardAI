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

for i, (train_feat, live_feat) \
      in enumerate(zip(training_features, live_features)):
    if train_feat != live_feat:
        print("\nMismatch Found")
        print("Position:", i)
        print("Training :", train_feat)
        print("Live     :", live_feat)
        break

