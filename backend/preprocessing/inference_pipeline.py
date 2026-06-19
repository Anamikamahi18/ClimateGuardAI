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


from datetime import datetime


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
