from fastapi import FastAPI

from backend.api.heatwave import router as heatwave_router

from backend.api.rainfall import router as rainfall_router

from backend.api import climate_risk

app = FastAPI(title="ClimateGuard AI", version="1.0")

app.include_router(heatwave_router)

app.include_router(rainfall_router)

app.include_router(
    climate_risk.router,
    prefix="/climate-risk",
    tags=["Climate Risk"]
)


@app.get("/")
def home():

    return {"message": "ClimateGuard AI Backend Running"}



