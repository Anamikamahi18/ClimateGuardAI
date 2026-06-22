from backend.preprocessing.inference_pipeline import (
    create_datetime_features, create_day_period, create_season
)

dt = create_datetime_features()

print(dt)

print(create_day_period(dt["hour"]))

print(create_season(dt["month"]))
