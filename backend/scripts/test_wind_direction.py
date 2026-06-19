from backend.preprocessing.inference_pipeline import *

result = create_wind_direction_features(280)

print(result)

print(sum(result.values()))
