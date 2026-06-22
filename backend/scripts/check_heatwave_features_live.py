from backend.services.weather_service import (
    get_coordinates,
    get_weather_data,
    get_air_quality_data,
)

from backend.preprocessing.inference_pipeline import build_heatwave_features

location = get_coordinates("Kochi")

weather = get_weather_data(location["latitude"], location["longitude"])

air = get_air_quality_data(location["latitude"], location["longitude"])

features = build_heatwave_features(weather, air, location)

important = [
    "temperature_celsius",
    "humidity",
    "pressure_mb",
    "heatwave_index",
    "wind_humidity_interaction",
    "humidity_cloud_interaction",
    "pm_difference",
    "pollution_intensity",
    "precip_mm",
]

for f in important:
    print(f, "=", features[f])
