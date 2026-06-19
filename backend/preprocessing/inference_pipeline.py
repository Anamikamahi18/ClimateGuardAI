from datetime import datetime


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
