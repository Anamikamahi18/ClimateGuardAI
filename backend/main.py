from fastapi import FastAPI

app = FastAPI(title="ClimateGuard AI", version="1.0")


@app.get("/")
def home():

    return {"message": "ClimateGuard AI Backend Running"}
