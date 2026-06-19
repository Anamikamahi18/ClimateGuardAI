from backend.preprocessing.inference_pipeline import *

dt = create_datetime_features()

print(dt)

print(create_day_period(dt["hour"]))

print(create_season(dt["month"]))
