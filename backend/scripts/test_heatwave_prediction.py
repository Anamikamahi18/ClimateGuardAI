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
print("HEATWAVE PREDICTION TEST")
print("=" * 60)

encoder = joblib.load("models/heatwave_label_encoder.pkl")

model = joblib.load("models/xgboost_heatwave_model.pkl")

location = get_coordinates("Kochi")

weather = get_weather_data(location["latitude"], location["longitude"])

air = get_air_quality_data(location["latitude"], location["longitude"])

features = build_heatwave_features(weather, air, location)

X = align_heatwave_features(features)

prediction = model.predict(X)[0]

risk = encoder.inverse_transform([prediction])[0]

print()
print("City : Kochi")
print("Prediction :", prediction)
print("Risk :", risk)
