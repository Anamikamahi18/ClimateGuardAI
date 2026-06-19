from backend.preprocessing.inference_pipeline import *

print(calculate_pm_difference(43.7, 51.7))

print(calculate_pollution_intensity(43.7, 51.7))

print(calculate_wind_humidity_interaction(6, 84))

print(calculate_humidity_cloud_interaction(84, 99))

print(calculate_temperature_gap(33.1, 27.6))

print(calculate_heatwave_index(27.6, 84))
