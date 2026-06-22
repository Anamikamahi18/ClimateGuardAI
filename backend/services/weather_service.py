import requests

from fastapi import HTTPException

from cachetools import TTLCache

# ==========================================
# CACHE CONFIGURATION
# ==========================================

weather_cache = TTLCache(maxsize=100, ttl=600)  # 10 minutes

air_cache = TTLCache(maxsize=100, ttl=600)  # 10 minutes


# ==========================================
# GEOCODING
# ==========================================


def get_coordinates(city: str):

    url = "https://geocoding-api.open-meteo.com/v1/search" \
        f"?name={city}&count=1"

    response = requests.get(url)

    response.raise_for_status()

    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found")

    result = data["results"][0]

    return {
        "city": result["name"],
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "country": result.get("country", ""),
    }


# ==========================================
# WEATHER DATA
# ==========================================


def get_weather_data(latitude: float, longitude: float):

    cache_key = f"{latitude}_{longitude}"

    # ---------------------------
    # CACHE HIT
    # ---------------------------

    if cache_key in weather_cache:
        print(f"Weather Cache Hit: {cache_key}")
        return weather_cache[cache_key]

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current=temperature_2m"
        "&current=relative_humidity_2m"
        "&current=apparent_temperature"
        "&current=pressure_msl"
        "&current=cloud_cover"
        "&current=visibility"
        "&current=wind_speed_10m"
        "&current=wind_direction_10m"
        "&current=uv_index"
    )

    response = requests.get(url, timeout=30)

    # ---------------------------
    # RATE LIMIT HANDLING
    # ---------------------------

    if response.status_code == 429:

        raise HTTPException(
            status_code=429,
            detail=(
                "Weather API rate limit exceeded. "
                "Please try again in a few minutes."
            ),
        )

    response.raise_for_status()

    data = response.json()

    current = data["current"]

    weather_data = {
        "temperature_2m": current["temperature_2m"],
        "relative_humidity_2m": current["relative_humidity_2m"],
        "apparent_temperature": current["apparent_temperature"],
        "pressure_msl": current["pressure_msl"],
        "cloud_cover": current["cloud_cover"],
        "visibility": current["visibility"],
        "wind_speed_10m": current["wind_speed_10m"],
        "wind_direction_10m": current["wind_direction_10m"],
        "uv_index": current["uv_index"],
    }

    # ---------------------------
    # SAVE TO CACHE
    # ---------------------------

    weather_cache[cache_key] = weather_data

    return weather_data


# ==========================================
# AIR QUALITY DATA
# ==========================================


def get_air_quality_data(latitude: float, longitude: float):

    cache_key = f"{latitude}_{longitude}"

    # ---------------------------
    # CACHE HIT
    # ---------------------------

    if cache_key in air_cache:
        print(f"Air Cache Hit: {cache_key}")
        return air_cache[cache_key]

    url = (
        "https://air-quality-api.open-meteo.com/v1/air-quality"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current=pm10"
        "&current=pm2_5"
        "&current=carbon_monoxide"
        "&current=nitrogen_dioxide"
        "&current=sulphur_dioxide"
        "&current=ozone"
    )

    response = requests.get(url, timeout=30)

    # ---------------------------
    # RATE LIMIT HANDLING
    # ---------------------------

    if response.status_code == 429:

        raise HTTPException(
            status_code=429,
            detail=(
                "Air Quality API rate limit exceeded. "
                "Please try again in a few minutes."
            ),
        )

    response.raise_for_status()

    data = response.json()

    current = data["current"]

    air_data = {
        "pm10": current["pm10"],
        "pm2_5": current["pm2_5"],
        "carbon_monoxide": current["carbon_monoxide"],
        "nitrogen_dioxide": current["nitrogen_dioxide"],
        "sulphur_dioxide": current["sulphur_dioxide"],
        "ozone": current["ozone"],
    }

    # ---------------------------
    # SAVE TO CACHE
    # ---------------------------

    air_cache[cache_key] = air_data

    return air_data
