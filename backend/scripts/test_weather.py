from backend.services.weather_service import get_coordinates, get_weather_data

city = "Kochi"

location = get_coordinates(city)

weather = get_weather_data(location["latitude"], location["longitude"])

print(weather)
