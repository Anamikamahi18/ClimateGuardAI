from backend.preprocessing.inference_pipeline import (
    build_rainfall_features,
    align_rainfall_features,
)

from backend.services.model_loader import (
    rainfall_model,
    rainfall_mapping,
)


from backend.services.weather_service import (
    get_coordinates,
    get_weather_data,
    get_air_quality_data,
)


def predict_rainfall_risk(city: str):

    location = get_coordinates(city)

    weather = get_weather_data(
        location["latitude"],
        location["longitude"],
    )

    air = get_air_quality_data(
        location["latitude"],
        location["longitude"],
    )

    return predict_rainfall_risk_from_data(
        weather,
        air,
        location,
    )


def predict_rainfall_risk_from_data(
    weather: dict,
    air: dict,
    location: dict,
):

    features = build_rainfall_features(
        weather,
        air,
        location,
    )

    X = align_rainfall_features(features)

    prediction = rainfall_model.predict(X)[0]

    rainfall_risk = rainfall_mapping[prediction]

    return {
        "city": location["name"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "rainfall_risk": rainfall_risk,
        "temperature_celsius": weather["temperature_2m"],
        "humidity": weather["relative_humidity_2m"],
        "cloud_cover": weather["cloud_cover"],
    }
