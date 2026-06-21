from fastapi import FastAPI

from backend.api.heatwave import (
    router as heatwave_router
)

from backend.api.rainfall import (
    router as rainfall_router
)

from backend.api.climate_profile import (
    router as climate_profile_router
)

from backend.api.anomaly import (
    router as anomaly_router
)

from backend.api import climate_risk

from backend.api.explainability import (
    router as explain_router
)

app = FastAPI(
    title="ClimateGuard AI",
    version="1.0"
)

app.include_router(
    heatwave_router
)

app.include_router(
    rainfall_router
)

app.include_router(
    climate_profile_router,
    prefix="/climate-profile",
    tags=["Climate Profile"]
)

app.include_router(
    anomaly_router,
    prefix="/anomaly",
    tags=["Anomaly Detection"]
)

app.include_router(
    climate_risk.router,
    prefix="/climate-risk",
    tags=["Climate Risk"]
)

app.include_router(
    explain_router,
    prefix="/explainability",
    tags=["Explainability"]
)


@app.get("/")
def home():

    return {
        "message":
        "ClimateGuard AI Backend Running"
    }
