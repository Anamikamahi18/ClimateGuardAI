import joblib
from backend.services.weather_service import (
    get_coordinates,
    get_weather_data,
    get_air_quality_data,
)
from backend.preprocessing.inference_pipeline import (
    build_heatwave_features, align_heatwave_features
)

heatwave_features = joblib.load("models/heatwave_feature_names.pkl")

print("Heatwave Feature Count:", len(heatwave_features))

print(heatwave_features[:20])


training_features = joblib.load("models/heatwave_feature_names.pkl")

location = get_coordinates("Kochi")

weather = get_weather_data(location["latitude"], location["longitude"])

air = get_air_quality_data(location["latitude"], location["longitude"])

features = build_heatwave_features(weather, air, location)

live_features = list(features.keys())

missing = set(training_features) - set(live_features)

extra = set(live_features) - set(training_features)

print("Missing:", len(missing))
print(missing)

print()

print("Extra:", len(extra))
print(extra)


model = joblib.load("models/xgboost_heatwave_model.pkl")

location = get_coordinates("Kochi")

weather = get_weather_data(location["latitude"], location["longitude"])

air = get_air_quality_data(location["latitude"], location["longitude"])

features = build_heatwave_features(weather, air, location)

X = align_heatwave_features(features)

prediction = model.predict(X)[0]

print(prediction)
