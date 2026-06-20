import joblib

from backend.services.weather_service import (
    get_coordinates,
    get_weather_data,
    get_air_quality_data,
)

from backend.preprocessing.inference_pipeline import (
    build_rainfall_features,
    align_rainfall_features,
)

rainfall_model = joblib.load("models/xgboost_rainfall_model.pkl")

rainfall_mapping = joblib.load("models/rainfall_class_mapping.pkl")


def predict_rainfall_risk(city: str):

    location = get_coordinates(city)

    weather = get_weather_data(location["latitude"], location["longitude"])

    air = get_air_quality_data(location["latitude"], location["longitude"])

    features = build_rainfall_features(weather, air, location)

    X = align_rainfall_features(features)

    prediction = rainfall_model.predict(X)[0]

    risk = rainfall_mapping[prediction]

    return {"city": city, "rainfall_risk": risk}
