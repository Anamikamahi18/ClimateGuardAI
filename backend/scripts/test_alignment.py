from backend.services.weather_service import get_coordinates, \
    get_weather_data, get_air_quality_data
from backend.preprocessing.inference_pipeline import build_rainfall_features, \
    align_rainfall_features

location = get_coordinates("Kochi")

weather = get_weather_data(location["latitude"], location["longitude"])

air = get_air_quality_data(location["latitude"], location["longitude"])

features = build_rainfall_features(weather, air, location)

df = align_rainfall_features(features)

print(df.shape)

print(df.columns.tolist()[:25])
