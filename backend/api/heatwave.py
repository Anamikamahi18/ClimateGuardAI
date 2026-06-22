from fastapi import APIRouter

from backend.services.heatwave_service import (
    predict_heatwave,
)

router = APIRouter(prefix="/heatwave", tags=["Heatwave"])


@router.get("/{city}")
def heatwave_prediction(city: str):
    try:
        return predict_heatwave(city)

    except ValueError as e:
        return {"error": str(e)}
