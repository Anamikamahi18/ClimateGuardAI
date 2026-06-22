import requests
import time
import urllib3

# Disable SSL warnings for fallback
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Fallback data for when APIs fail
FALLBACK_WEATHER = {
    "temperature_2m": 28.0,
    "relative_humidity_2m": 65,
    "apparent_temperature": 32.0,
    "pressure_msl": 1013.25,
    "cloud_cover": 40,
    "visibility": 10000,
    "wind_speed_10m": 12.0,
    "wind_direction_10m": 180,
    "uv_index": 6.5,
}

FALLBACK_AIR_QUALITY = {
    "pm10": 50.0,
    "pm2_5": 30.0,
    "carbon_monoxide": 300.0,
    "nitrogen_dioxide": 40.0,
    "sulphur_dioxide": 10.0,
    "ozone": 60.0,
}


def retry_request(url, params=None, max_retries=3, timeout=10):
    """Make HTTP request with retry logic and fallback."""
    for attempt in range(max_retries):
        try:
            response = requests.get(
                url,
                params=params,
                timeout=timeout,
                verify=False,  # Disable SSL verification to handle cert issues
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"⏱️ Timeout on attempt {attempt + 1}/{max_retries}")
            if attempt < max_retries - 1:
                time.sleep(2**attempt)  # Exponential backoff
        except requests.exceptions.ConnectionError as e:
            print(
                "🔌 Connection error on attempt "
                f"{attempt + 1}/{max_retries}: {str(e)}"
            )
            if attempt < max_retries - 1:
                time.sleep(2**attempt)
        except requests.exceptions.RequestException as e:
            print(
                f"❌ Request error on attempt "
                f"{attempt + 1}/{max_retries}: {str(e)}"
            )
            if attempt < max_retries - 1:
                time.sleep(2**attempt)

    return None


def get_coordinates(city: str):
    """Get city coordinates from Open-Meteo geocoding API."""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 10, "language": "en", "format": "json"}

    data = retry_request(url, params)

    if not data or "results" not in data:
        raise ValueError(f"❌ City not found: {city}")

    for result in data["results"]:
        country = result.get("country", "")
        if country.lower() == "india":
            return {
                "latitude": result["latitude"],
                "longitude": result["longitude"],
                "name": result["name"],
                "country": country,
            }

    raise ValueError(f"❌ No Indian city found for {city}")


def get_weather_data(latitude: float, longitude: float):
    """Get current weather data with fallback."""
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

    data = retry_request(url, params, max_retries=3, timeout=10)

    if data:
        print("✅ Weather data retrieved successfully")
        return data["current"]
    else:
        print("⚠️ Weather API failed, using fallback data")
        return FALLBACK_WEATHER


def get_air_quality_data(latitude: float, longitude: float):
    """Get air quality data with fallback."""
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

    data = retry_request(url, params, max_retries=3, timeout=10)

    if data:
        print("✅ Air quality data retrieved successfully")
        return data["current"]
    else:
        print("⚠️ Air quality API failed, using fallback data")
        return FALLBACK_AIR_QUALITY
