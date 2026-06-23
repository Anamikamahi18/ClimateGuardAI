from backend.services.model_loader import (
    heatwave_model,
    heatwave_encoder,
)

from backend.services.weather_service import (
    get_coordinates,
    get_weather_data,
    get_air_quality_data,
)

from backend.preprocessing.inference_pipeline import (
    build_heatwave_features,
    align_heatwave_features,
)


def predict_heatwave(
    city: str,
    location: dict = None,
    weather: dict = None,
    air: dict = None,
):
    """
    Supports:
    1. Standalone endpoint calls
    2. Shared data from complete analysis
    """

    # ==========================================
    # FETCH ONLY IF NOT PROVIDED
    # ==========================================

    if location is None:
        location = get_coordinates(city)

    if weather is None:
        weather = get_weather_data(
            location["latitude"],
            location["longitude"],
        )

    if air is None:
        air = get_air_quality_data(
            location["latitude"],
            location["longitude"],
        )

    # ==========================================
    # FEATURE ENGINEERING
    # ==========================================

    features = build_heatwave_features(
        weather,
        air,
        location,
    )

    X = align_heatwave_features(
        features
    )

    # ==========================================
    # PREDICTION
    # ==========================================

    prediction = heatwave_model.predict(X)[0]

    risk = heatwave_encoder.inverse_transform(
        [prediction]
    )[0]

    # ==========================================
    # RESPONSE
    # ==========================================

    return {
        "city": city,
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "heatwave_risk": risk,
        "temperature_celsius": weather["temperature_2m"],
        "humidity": weather["relative_humidity_2m"],
        "uv_index": weather["uv_index"],
    }
