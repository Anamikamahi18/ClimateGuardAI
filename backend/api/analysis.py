from fastapi import APIRouter, HTTPException

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
    try:
        city = request.city

        # ==========================================
        # LOCATION
        # ==========================================
        try:
            location = get_coordinates(city)
        except ValueError:
            raise HTTPException(
                status_code=404,
                detail=f"City not found: {city}",
            )

        latitude = location["latitude"]
        longitude = location["longitude"]

        # ==========================================
        # LIVE DATA (with fallback)
        # ==========================================
        try:
            weather = get_weather_data(latitude, longitude)
            air = get_air_quality_data(latitude, longitude)
        except Exception as e:
            print(f"⚠️ Error fetching live data: {str(e)}")
            raise HTTPException(
                status_code=503,
                detail=(
                    "Weather data service temporarily unavailable. "
                    "Using fallback data."
                ),
            )

        # ==========================================
        # FEATURES
        # ==========================================
        try:
            rainfall_features = build_rainfall_features(weather, air, location)

            heatwave_features = build_heatwave_features(weather, air, location)

            rainfall_X = align_rainfall_features(rainfall_features)

            heatwave_X = align_heatwave_features(heatwave_features)
        except Exception as e:
            print(f"❌ Feature engineering error: {str(e)}")
            raise HTTPException(
                status_code=400, detail=f"Feature engineering failed: {str(e)}"
            )

        # ==========================================
        # RAINFALL
        # ==========================================
        try:
            rainfall_result = predict_rainfall_risk(rainfall_X)
        except Exception as e:
            print(f"❌ Rainfall prediction error: {str(e)}")
            rainfall_result = {
                "prediction": "Unknown",
                "confidence": 0,
                "error": str(e),
            }

        # ==========================================
        # HEATWAVE
        # ==========================================
        try:
            heatwave_result = predict_heatwave(heatwave_X)
        except Exception as e:
            print(f"❌ Heatwave prediction error: {str(e)}")
            heatwave_result = {
                "prediction": "Unknown",
                "confidence": 0,
                "error": str(e),
            }

        # ==========================================
        # CLIMATE PROFILE
        # ==========================================
        try:
            climate_profile_result = predict_climate_profile(rainfall_features)
        except Exception as e:
            print(f"❌ Climate profile error: {str(e)}")
            climate_profile_result = {
                "climate_cluster": -1,
                "climate_profile": "Unknown",
            }

        # ==========================================
        # ANOMALY DETECTION
        # ==========================================
        try:
            anomaly_result = predict_anomaly(rainfall_features)
        except Exception as e:
            print(f"❌ Anomaly detection error: {str(e)}")
            anomaly_result = {"anomaly_status": "Unknown"}

        # ==========================================
        # CLIMATE RISK
        # ==========================================
        try:
            climate_risk = calculate_climate_risk(
                rainfall_result, heatwave_result, climate_profile_result
            )
        except Exception as e:
            print(f"❌ Climate risk error: {str(e)}")
            climate_risk = {"category": "Unknown", "score": 0}

        # ==========================================
        # EXPLAINABILITY
        # ==========================================
        try:
            rainfall_explanation = explain_rainfall_prediction(
                rainfall_features,
                rainfall_result,
            )
            heatwave_explanation = explain_heatwave_prediction(
                heatwave_features,
                heatwave_result,
            )
        except Exception as e:
            print(f"⚠️ Explainability error: {str(e)}")
            rainfall_explanation = {"risk_drivers": []}
            heatwave_explanation = {"risk_drivers": []}

        # ==========================================
        # RESPONSE
        # ==========================================
        return {
            "city": city,
            "coordinates": {
                "latitude": latitude,
                "longitude": longitude,
            },
            "rainfall": rainfall_result,
            "heatwave": heatwave_result,
            "climate_risk": climate_risk,
            "climate_profile": climate_profile_result.get(
                "climate_profile",
                "Unknown",
            ),
            "anomaly_status": anomaly_result.get("anomaly_status", "Unknown"),
            "explanations": {
                "rainfall": rainfall_explanation,
                "heatwave": heatwave_explanation,
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Unexpected error in analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}",
        )
