from fastapi import APIRouter

from backend.schemas.analysis import AnalysisRequest

from backend.services.weather_service import (
    get_coordinates,
    get_weather_data,
    get_air_quality_data,
)

from backend.preprocessing.inference_pipeline import (
    build_rainfall_features,
    build_heatwave_features,
    align_rainfall_features,
    align_heatwave_features,
)

from backend.services.rainfall_service import (
    predict_rainfall_risk,
)

from backend.services.heatwave_service import (
    predict_heatwave,
)

from backend.services.climate_profile_service import (
    predict_climate_profile,
)

from backend.services.anomaly_service import (
    predict_anomaly,
)

from backend.services.climate_service import (
    calculate_climate_risk,
)

from backend.services.shap_service import (
    explain_rainfall_prediction,
    explain_heatwave_prediction,
)

router = APIRouter()


@router.post("/complete")
def complete_analysis(request: AnalysisRequest):

    city = request.city

    # ==========================================
    # LOCATION
    # ==========================================

    location = get_coordinates(city)

    latitude = location["latitude"]
    longitude = location["longitude"]

    # ==========================================
    # LIVE DATA
    # ==========================================

    weather = get_weather_data(
        latitude,
        longitude
    )

    air = get_air_quality_data(
        latitude,
        longitude
    )

    # ==========================================
    # FEATURES
    # ==========================================

    rainfall_features = build_rainfall_features(
        weather,
        air,
        location
    )

    heatwave_features = build_heatwave_features(
        weather,
        air,
        location
    )

    rainfall_X = align_rainfall_features(
        rainfall_features
    )

    heatwave_X = align_heatwave_features(
        heatwave_features
    )

    # ==========================================
    # RAINFALL
    # ==========================================

    rainfall_result = predict_rainfall_risk(city)

    # ==========================================
    # HEATWAVE
    # ==========================================

    heatwave_result = predict_heatwave(city)

    # ==========================================
    # CLIMATE PROFILE
    # ==========================================

    climate_profile = predict_climate_profile(
        rainfall_features
    )

    # ==========================================
    # ANOMALY
    # ==========================================

    anomaly_result = predict_anomaly(
        rainfall_features
    )

    # ==========================================
    # CLIMATE RISK
    # ==========================================

    risk_result = calculate_climate_risk(
        rainfall_result["rainfall_risk"],
        heatwave_result["heatwave_risk"],
        anomaly_result["anomaly_status"],
        climate_profile["climate_profile"],
    )

    # ==========================================
    # SHAP
    # ==========================================

    rainfall_explanation = (
        explain_rainfall_prediction(
            rainfall_X
        )
    )

    heatwave_explanation = (
        explain_heatwave_prediction(
            heatwave_X
        )
    )

    # ==========================================
    # RESPONSE
    # ==========================================

    return {
        "city": city,

        "coordinates": {
            "latitude": latitude,
            "longitude": longitude,
        },

        "climate_profile":
            climate_profile["climate_profile"],

        "anomaly_status":
            anomaly_result["anomaly_status"],

        "rainfall": {
            "prediction":
                rainfall_explanation["prediction"],

            "confidence":
                rainfall_explanation["confidence"],
        },

        "heatwave": {
            "prediction":
                heatwave_explanation["prediction"],

            "confidence":
                heatwave_explanation["confidence"],
        },

        "climate_risk": {
            "score":
                risk_result["climate_risk_score"],

            "category":
                risk_result["climate_risk"],
        },

        "explanations": {
            "rainfall":
                rainfall_explanation,

            "heatwave":
                heatwave_explanation,
        },
    }
