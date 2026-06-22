import joblib

from backend.services.weather_service import (
    get_coordinates,
    get_weather_data,
    get_air_quality_data,
)

from backend.preprocessing.inference_pipeline import (
    build_heatwave_features,
    align_heatwave_features,
)

print("=" * 60)
print("HEATWAVE FEATURE ALIGNMENT CHECK")
print("=" * 60)

training_features = joblib.load("models/heatwave_feature_names.pkl")

print()
print("Training Feature Count:")
print(len(training_features))

location = get_coordinates("Kochi")

weather = get_weather_data(location["latitude"], location["longitude"])

air = get_air_quality_data(location["latitude"], location["longitude"])

features = build_heatwave_features(weather, air, location)

live_features = list(features.keys())

missing = set(training_features) - set(live_features)

extra = set(live_features) - set(training_features)

print()
print("Missing Features:")
print(len(missing))
print(missing)

print()
print("Extra Features:")
print(len(extra))
print(extra)

X = align_heatwave_features(features)

print()
print("Aligned Shape:")
print(X.shape)

if len(missing) == 0 and len(extra) == 0:
    print()
    print("Feature Alignment Passed")
else:
    print()
    print("Feature Alignment Failed")
