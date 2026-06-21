from fastapi import FastAPI

from backend.api.heatwave import router as heatwave_router

app = FastAPI(title="ClimateGuard AI", version="1.0")

app.include_router(heatwave_router)


@app.get("/")
def home():

    return {"message": "ClimateGuard AI Backend Running"}
