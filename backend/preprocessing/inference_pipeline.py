from datetime import datetime
import pandas as pd
import joblib


def calculate_pm_difference(pm25, pm10):
    return abs(pm10 - pm25)


def calculate_pollution_intensity(pm25, pm10):
    return (pm25 + pm10) / 2


def calculate_wind_humidity_interaction(wind_kph, humidity):
    return wind_kph * humidity


def calculate_humidity_cloud_interaction(humidity, cloud):
    return humidity * cloud


def calculate_temperature_gap(feels_like, temperature):
    return feels_like - temperature


def calculate_heatwave_index(temperature, humidity):
    return temperature + ((humidity / 100) * temperature)


def create_datetime_features():

    now = datetime.now()

    return {
        "year": now.year,
        "month": now.month,
        "day": now.day,
        "hour": now.hour,
        "weekday": now.weekday(),
    }


def create_day_period(hour):

    if 6 <= hour < 18:
        return {"day_period_1": 1, "day_period_2": 0}

    return {"day_period_1": 0, "day_period_2": 1}


def create_season(month):

    season = {"season_1": 0, "season_2": 0, "season_3": 0}

    if month in [3, 4, 5, 6]:
        season["season_1"] = 1

    elif month in [7, 8, 9, 10]:
        season["season_2"] = 1

    else:
        season["season_3"] = 1

    return season


def create_wind_direction_features(wind_degree):

    directions = {
        "wind_direction_1": 0,
        "wind_direction_2": 0,
        "wind_direction_3": 0,
        "wind_direction_4": 0,
        "wind_direction_5": 0,
        "wind_direction_6": 0,
        "wind_direction_7": 0,
        "wind_direction_8": 0,
        "wind_direction_9": 0,
        "wind_direction_10": 0,
        "wind_direction_11": 0,
        "wind_direction_12": 0,
        "wind_direction_13": 0,
        "wind_direction_14": 0,
        "wind_direction_15": 0,
    }

    sector = int(wind_degree / 24)

    sector = min(sector, 14)

    directions[f"wind_direction_{sector + 1}"] = 1

    return directions


def create_default_region_features():

    return {f"region_{i}": 0 for i in range(1, 33)}


def create_default_timezone_features():

    return {"timezone_1": 0, "timezone_2": 0}


def create_default_moon_features():

    moon = {"moon_illumination": 50}

    for i in range(1, 8):
        moon[f"moon_phase_{i}"] = 0

    moon["moon_phase_1"] = 1

    return moon


def create_default_day_length():

    return {"day_length_minutes": 720}


def build_rainfall_features(weather_data, air_quality_data, location_data):

    features = {}

    # ==========================
    # BASIC WEATHER
    # ==========================

    temperature = weather_data["temperature_2m"]
    humidity = weather_data["relative_humidity_2m"]
    pressure = weather_data["pressure_msl"]
    cloud = weather_data["cloud_cover"]

    visibility_km = weather_data["visibility"] / 1000

    wind_kph = weather_data["wind_speed_10m"]

    wind_degree = weather_data["wind_direction_10m"]

    feels_like = weather_data["apparent_temperature"]

    # ==========================
    # RAW FEATURES
    # ==========================

    features["latitude"] = location_data["latitude"]
    features["longitude"] = location_data["longitude"]

    features["temperature_celsius"] = temperature

    features["wind_kph"] = wind_kph
    features["wind_degree"] = wind_degree

    features["pressure_mb"] = pressure

    features["humidity"] = humidity
    features["cloud"] = cloud

    features["feels_like_celsius"] = feels_like

    features["visibility_km"] = visibility_km

    features["uv_index"] = weather_data["uv_index"]

    features["gust_kph"] = wind_kph

    # ==========================
    # AIR QUALITY
    # ==========================

    pm25 = air_quality_data["pm2_5"]
    pm10 = air_quality_data["pm10"]

    features["air_quality_Carbon_Monoxide"] = \
        air_quality_data["carbon_monoxide"]

    features["air_quality_Ozone"] = air_quality_data["ozone"]

    features["air_quality_Nitrogen_dioxide"] = \
        air_quality_data["nitrogen_dioxide"]

    features["air_quality_Sulphur_dioxide"] = \
        air_quality_data["sulphur_dioxide"]

    features["air_quality_PM2.5"] = pm25

    features["air_quality_PM10"] = pm10

    features["air_quality_us-epa-index"] = 3

    features["air_quality_gb-defra-index"] = 6

    # ==========================
    # ENGINEERED FEATURES
    # ==========================

    features["temperature_gap"] = (
        calculate_temperature_gap(
            feels_like,
            temperature
            )
            )

    features["pm_difference"] = (
        calculate_pm_difference(
            pm25,
            pm10
            )
            )

    features["pollution_intensity"] = (
        calculate_pollution_intensity(
            pm25,
            pm10
            )
            )

    features["wind_humidity_interaction"] = (
        calculate_wind_humidity_interaction(
            wind_kph,
            humidity
            )
            )

    features["humidity_cloud_interaction"] = (
        calculate_humidity_cloud_interaction(
            humidity,
            cloud
            )
            )

    features["heatwave_index"] = (
        calculate_heatwave_index(
            temperature,
            humidity
            )
            )

    # ==========================
    # DATETIME FEATURES
    # ==========================

    dt = create_datetime_features()

    features.update(dt)

    features.update(
        create_day_period(
            dt["hour"]
        )
        )

    features.update(
        create_season(
            dt["month"]
        )
        )

    # ==========================
    # WIND DIRECTION
    # ==========================

    features.update(
        create_wind_direction_features(
            wind_degree
            )
            )

    # ==========================
    # DEFAULT FEATURES
    # ==========================

    features.update(
        create_default_region_features()
    )

    features.update(
        create_default_timezone_features()
        )

    features.update(
        create_default_moon_features()
        )

    features.update(
        create_default_day_length()
    )

    return features


def align_rainfall_features(features):

    feature_order = joblib.load("models/rainfall_feature_names.pkl")

    df = pd.DataFrame([features])

    for col in feature_order:
        if col not in df.columns:
            df[col] = 0

    df = df[feature_order]

    return df


def build_heatwave_features(weather_data, air_quality_data, location_data):

    features = {}

    temperature = weather_data["temperature_2m"]
    humidity = weather_data["relative_humidity_2m"]
    pressure = weather_data["pressure_msl"]
    cloud = weather_data["cloud_cover"]

    visibility_km = weather_data["visibility"] / 1000

    wind_kph = weather_data["wind_speed_10m"]

    wind_degree = weather_data["wind_direction_10m"]

    pm25 = air_quality_data["pm2_5"]
    pm10 = air_quality_data["pm10"]

    # =====================
    # RAW FEATURES
    # =====================

    features["latitude"] = location_data["latitude"]
    features["longitude"] = location_data["longitude"]

    features["temperature_celsius"] = temperature

    features["wind_kph"] = wind_kph
    features["wind_degree"] = wind_degree

    features["pressure_mb"] = pressure

    # Heatwave-specific feature
    features["precip_mm"] = 0

    features["humidity"] = humidity
    features["cloud"] = cloud

    features["visibility_km"] = visibility_km

    features["uv_index"] = weather_data["uv_index"]

    features["gust_kph"] = wind_kph

    # =====================
    # AIR QUALITY
    # =====================

    features["air_quality_Carbon_Monoxide"] = \
        air_quality_data["carbon_monoxide"]

    features["air_quality_Ozone"] = air_quality_data["ozone"]

    features["air_quality_Nitrogen_dioxide"] = \
        air_quality_data["nitrogen_dioxide"]

    features["air_quality_Sulphur_dioxide"] = \
        air_quality_data["sulphur_dioxide"]

    features["air_quality_PM2.5"] = pm25

    features["air_quality_PM10"] = pm10

    features["air_quality_us-epa-index"] = 3

    features["air_quality_gb-defra-index"] = 6

    # =====================
    # ENGINEERED FEATURES
    # =====================

    features["pm_difference"] = calculate_pm_difference(pm25, pm10)

    features["pollution_intensity"] = calculate_pollution_intensity(pm25, pm10)

    features["wind_humidity_interaction"] = \
        calculate_wind_humidity_interaction(
        wind_kph, humidity
    )

    features["humidity_cloud_interaction"] = \
        calculate_humidity_cloud_interaction(
        humidity, cloud
    )

    features["heatwave_index"] = \
        calculate_heatwave_index(temperature, humidity)

    # =====================
    # DATETIME
    # =====================

    dt = create_datetime_features()

    features.update(dt)

    features.update(create_day_period(dt["hour"]))

    features.update(create_season(dt["month"]))

    # =====================
    # ENCODINGS
    # =====================

    features.update(create_wind_direction_features(wind_degree))

    features.update(create_default_region_features())

    features.update(create_default_timezone_features())

    features.update(create_default_moon_features())

    features.update(create_default_day_length())

    return features


def align_heatwave_features(features):

    import joblib
    import pandas as pd

    feature_order = joblib.load("models/heatwave_feature_names.pkl")

    df = pd.DataFrame([features])

    for col in feature_order:
        if col not in df.columns:
            df[col] = 0

    df = df[feature_order]

    return df
