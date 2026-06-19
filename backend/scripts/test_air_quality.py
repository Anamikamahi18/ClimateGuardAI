from backend.services.weather_service import get_coordinates, \
    get_air_quality_data

city = "Kochi"

location = get_coordinates(city)

air_quality = get_air_quality_data(location["latitude"], location["longitude"])

print(air_quality)
