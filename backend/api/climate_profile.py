from fastapi import APIRouter

from backend.services.weather_service import (
    get_coordinates,
    get_weather_data,
    get_air_quality_data,
)

from backend.preprocessing.inference_pipeline import (
    build_rainfall_features,
)

from backend.services.climate_profile_service import (
    predict_climate_profile,
)

router = APIRouter()


@router.get("/{city}")
def climate_profile(city: str):

    location = get_coordinates(city)

    weather = get_weather_data(location["latitude"], location["longitude"])

    air = get_air_quality_data(location["latitude"], location["longitude"])

    features = build_rainfall_features(weather, air, location)

    print(features.keys())

    result = predict_climate_profile(features)

    return {
        "city": city,
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "climate_cluster": result["climate_cluster"],
        "climate_profile": result["climate_profile"],
    }
