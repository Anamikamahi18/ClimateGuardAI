from backend.services.weather_service import (
    get_coordinates,
    get_weather_data,
    get_air_quality_data,
)

from backend.services.model_loader import (
    heatwave_model,
    heatwave_encoder,
)

from backend.preprocessing.inference_pipeline import (
    build_heatwave_features,
    align_heatwave_features,
)


def predict_heatwave(city: str):

    location = get_coordinates(city)

    weather = get_weather_data(
        location["latitude"],
        location["longitude"],
    )

    air = get_air_quality_data(
        location["latitude"],
        location["longitude"],
    )

    return predict_heatwave_from_data(
        weather,
        air,
        location,
    )


def predict_heatwave_from_data(
    weather: dict,
    air: dict,
    location: dict,
):

    features = build_heatwave_features(
        weather,
        air,
        location,
    )

    X = align_heatwave_features(features)

    prediction = heatwave_model.predict(X)[0]

    heatwave_risk = heatwave_encoder.inverse_transform([prediction])[0]

    return {
        "city": location["name"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "heatwave_risk": heatwave_risk,
        "temperature_celsius": weather["temperature_2m"],
        "humidity": weather["relative_humidity_2m"],
        "uv_index": weather["uv_index"],
    }
