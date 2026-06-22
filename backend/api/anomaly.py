from fastapi import APIRouter

from backend.services.weather_service import (
    get_coordinates,
    get_weather_data,
    get_air_quality_data,
)

from backend.preprocessing.inference_pipeline import (
    build_rainfall_features,
)

from backend.services.anomaly_service import (
    predict_anomaly,
)

router = APIRouter()


@router.get("/{city}")
def anomaly(city: str):

    location = get_coordinates(city)

    weather = get_weather_data(
        location["latitude"],
        location["longitude"]
    )

    air = get_air_quality_data(
        location["latitude"],
        location["longitude"]
    )

    features = build_rainfall_features(
        weather,
        air,
        location
    )

    result = predict_anomaly(
        features
    )

    return {
        "city": city,
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "anomaly_flag": result["anomaly_flag"],
        "anomaly_status": result["anomaly_status"],
    }
