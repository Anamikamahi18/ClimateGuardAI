from backend.services.weather_service import get_coordinates, get_weather_data


print(get_coordinates("Kochi"))
print(get_coordinates("Mumbai"))
print(get_coordinates("Delhi"))
print(get_coordinates("Chennai"))


city = "Kochi"

location = get_coordinates(city)

weather = get_weather_data(
    location["latitude"],
    location["longitude"]
)

print(weather)
