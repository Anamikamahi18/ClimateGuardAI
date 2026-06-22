from backend.services.weather_service import (
    get_coordinates,
    get_weather_data,
    get_air_quality_data,
)

from backend.preprocessing.inference_pipeline import (
    build_heatwave_features,
)

print("=" * 50)
print("HEATWAVE FEATURE BUILDER TEST")
print("=" * 50)

location = get_coordinates("Kochi")

weather = get_weather_data(location["latitude"], location["longitude"])

air = get_air_quality_data(location["latitude"], location["longitude"])

features = build_heatwave_features(weather, air, location)

print()

print("Feature Count:")
print(len(features))

print()

for key, value in features.items():
    print(f"{key} : {value}")

print()

print("Heatwave Feature Builder Passed")
