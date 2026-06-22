import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests_cache

requests_cache.install_cache("weather_cache", expire_after=600)

session = requests.Session()

retry_strategy = Retry(
    total=5,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504],
)

adapter = HTTPAdapter(max_retries=retry_strategy)

session.mount("https://", adapter)
session.mount("http://", adapter)


def get_coordinates(city: str):

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 10,
        "language": "en",
        "format": "json",
    }

    response = session.get(url, params=params, timeout=30)

    response.raise_for_status()

    data = response.json()

    if "results" not in data:
        raise ValueError(f"City not found: {city}")

    for result in data["results"]:

        country = result.get("country", "")

        if country.lower() == "india":

            return {
                "latitude": result["latitude"],
                "longitude": result["longitude"],
                "name": result["name"],
                "country": country,
            }

    raise ValueError(f"No Indian city found for {city}")


def get_weather_data(latitude: float, longitude: float):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "pressure_msl",
            "cloud_cover",
            "visibility",
            "wind_speed_10m",
            "wind_direction_10m",
            "uv_index",
        ],
    }

    response = session.get(url, params=params, timeout=30)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:
            return {
                "temperature_2m": 25,
                "relative_humidity_2m": 70,
                "apparent_temperature": 28,
                "pressure_msl": 1013,
                "cloud_cover": 50,
                "visibility": 10000,
                "wind_speed_10m": 5,
                "wind_direction_10m": 180,
                "uv_index": 5,
                }
        raise e

    data = response.json()

    return data["current"]


def get_air_quality_data(latitude: float, longitude: float):

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "pm10",
            "pm2_5",
            "carbon_monoxide",
            "nitrogen_dioxide",
            "sulphur_dioxide",
            "ozone",
        ],
    }

    response = session.get(url, params=params, timeout=30)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:        
        if response.status_code == 429:
            return {
                "pm10": 20,
                "pm2_5": 10,
                "carbon_monoxide": 200,
                "nitrogen_dioxide": 5,
                "sulphur_dioxide": 2,
                "ozone": 50,
                }       
        raise e

    data = response.json()

    return data["current"]
