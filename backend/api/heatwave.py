from fastapi import APIRouter

from backend.services.heatwave_service import (
    predict_heatwave,
)

router = APIRouter(prefix="/heatwave", tags=["Heatwave"])


@router.get("/{city}")
def heatwave_prediction(city: str):

    return predict_heatwave(city)
