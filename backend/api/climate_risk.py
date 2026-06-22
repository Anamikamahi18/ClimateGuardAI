from fastapi import APIRouter

from backend.services.weather_service import (
    get_coordinates,
    get_weather_data,
    get_air_quality_data,
)

from backend.services.feature_engineering_service import build_features

from backend.services.rainfall_service import predict_rainfall_risk

from backend.services.heatwave_service import predict_heatwave

from backend.services.climate_profile_service import predict_climate_profile

from backend.services.anomaly_service import predict_anomaly

from backend.services.climate_service import calculate_climate_risk

router = APIRouter()


@router.get("/{city}")
def climate_risk(city: str):

    location = get_coordinates(city)

    latitude = location["latitude"]
    longitude = location["longitude"]

    weather = get_weather_data(latitude, longitude)

    air_quality = get_air_quality_data(latitude, longitude)

    features = build_features(weather, air_quality, location)

    rainfall_result = predict_rainfall_risk(city)

    heatwave_result = predict_heatwave(city)

    profile_result = predict_climate_profile(features)

    anomaly_result = predict_anomaly(features)

    risk_result = calculate_climate_risk(
        rainfall_result["rainfall_risk"],
        heatwave_result["heatwave_risk"],
        anomaly_result["anomaly_status"],
        profile_result["climate_profile"],
    )

    return {
        "city": city,
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "rainfall_risk": rainfall_result["rainfall_risk"],
        "heatwave_risk": heatwave_result["heatwave_risk"],
        "climate_profile": profile_result["climate_profile"],
        "anomaly_status": anomaly_result["anomaly_status"],
        "climate_risk_score": risk_result["climate_risk_score"],
        "climate_risk": risk_result["climate_risk"],
    }
