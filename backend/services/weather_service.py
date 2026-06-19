import requests


def get_coordinates(city: str):

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {"name": city, "count": 1, "language": "en", "format": "json"}

    response = requests.get(url, params=params, timeout=30)

    data = response.json()

    if "results" not in data:
        raise ValueError(f"City not found: {city}")

    result = data["results"][0]

    return {
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "name": result["name"],
    }
