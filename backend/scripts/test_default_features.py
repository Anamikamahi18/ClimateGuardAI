from backend.preprocessing.inference_pipeline import (
    create_default_region_features,
    create_default_timezone_features,
    create_default_moon_features,
    create_default_day_length,
)


print(len(create_default_region_features()))

print(create_default_timezone_features())

print(create_default_moon_features())

print(create_default_day_length())
