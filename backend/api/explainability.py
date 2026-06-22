from fastapi import APIRouter

from backend.schemas.explainability import ExplainabilityRequest

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

from backend.services.shap_service import (
    explain_rainfall_prediction,
    explain_heatwave_prediction,
)

router = APIRouter()


@router.post("/explain")
def explain(request: ExplainabilityRequest):

    location = get_coordinates(request.city)

    weather = get_weather_data(location["latitude"], location["longitude"])

    air = get_air_quality_data(location["latitude"], location["longitude"])

    rainfall_features = build_rainfall_features(weather, air, location)

    heatwave_features = build_heatwave_features(weather, air, location)

    rainfall_X = align_rainfall_features(rainfall_features)

    heatwave_X = align_heatwave_features(heatwave_features)

    rainfall_explanation = explain_rainfall_prediction(rainfall_X)

    for k, v in rainfall_explanation.items():
        print(k, type(v))

    heatwave_explanation = explain_heatwave_prediction(heatwave_X)

    for k, v in heatwave_explanation.items():
        print(k, type(v))

    return {
        "city": request.city,
        "rainfall": rainfall_explanation,
        "heatwave": heatwave_explanation,
    }
