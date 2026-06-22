from backend.services.weather_service import (
    get_coordinates,
    get_weather_data,
    get_air_quality_data,
)

from backend.preprocessing.inference_pipeline import (
    build_rainfall_features,
    align_rainfall_features,
)

from backend.services.model_loader import (
    rainfall_model,
    rainfall_mapping,
)


def predict_rainfall_risk(city: str):

    location = get_coordinates(city)

    weather = get_weather_data(location["latitude"], location["longitude"])

    air = get_air_quality_data(location["latitude"], location["longitude"])

    features = build_rainfall_features(weather, air, location)

    X = align_rainfall_features(features)

    prediction = rainfall_model.predict(X)[0]

    risk = rainfall_mapping[prediction]

    return {
        "city": city,
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "rainfall_risk": risk,
        "temperature_celsius": weather["temperature_2m"],
        "humidity": weather["relative_humidity_2m"],
        "cloud_cover": weather["cloud_cover"],
    }


def predict_rainfall_risk_from_features(features: dict):

    X = align_rainfall_features(features)

    prediction = rainfall_model.predict(X)[0]

    risk = rainfall_mapping[prediction]

    return {
        "rainfall_risk": risk,
        "prediction_code": int(prediction),
    }
