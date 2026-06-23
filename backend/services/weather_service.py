import time
import requests_cache

# ==================================================
# CACHE
# ==================================================

session = requests_cache.CachedSession(".cache", expire_after=300)

# ==================================================
# REQUEST HELPER
# ==================================================


def safe_get(url, params):
    """
    Retries requests if Open-Meteo returns 429.
    """

    for attempt in range(5):

        response = session.get(url, params=params, timeout=30)

        if response.status_code == 429:

            wait_time = 2**attempt

            print("Rate limited by Open-Meteo.")

            time.sleep(wait_time)

            continue

        response.raise_for_status()

        return response.json()

    raise Exception("Open-Meteo rate limit exceeded")


# ==================================================
# GEOCODING
# ==================================================


def get_coordinates(city: str):

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {"name": city, "count": 10, "language": "en", "format": "json"}

    data = safe_get(url, params)

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


# ==================================================
# WEATHER
# ==================================================


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

    data = safe_get(url, params)

    return data["current"]


# ==================================================
# AIR QUALITY
# ==================================================


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

    data = safe_get(url, params)

    return data["current"]
