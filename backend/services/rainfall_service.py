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


def predict_rainfall_risk(
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

    features = build_rainfall_features(
        weather,
        air,
        location,
    )

    X = align_rainfall_features(features)

    # ==========================================
    # PREDICTION
    # ==========================================

    prediction = rainfall_model.predict(X)[0]

    risk = rainfall_mapping[prediction]

    # ==========================================
    # RESPONSE
    # ==========================================

    return {
        "city": city,
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "rainfall_risk": risk,
        "temperature_celsius": weather["temperature_2m"],
        "humidity": weather["relative_humidity_2m"],
        "cloud_cover": weather["cloud_cover"],
    }
