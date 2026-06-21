from fastapi import APIRouter

from backend.services.rainfall_service import predict_rainfall_risk

router = APIRouter(prefix="/rainfall", tags=["Rainfall"])


@router.get("/{city}")
def rainfall_prediction(city: str):

    return predict_rainfall_risk(city)
