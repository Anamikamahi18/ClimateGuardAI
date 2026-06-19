import os
import joblib

files = [
    "models/xgboost_rainfall_model.pkl",
    "models/xgboost_heatwave_model.pkl",
    "models/rainfall_feature_names.pkl",
    "models/heatwave_feature_names.pkl",
    "models/rainfall_label_encoder.pkl",
    "models/heatwave_label_encoder.pkl",
]

for file in files:
    print(file, "->", os.path.exists(file))


mapping = joblib.load("models/rainfall_class_mapping.pkl")

print(type(mapping))
print(mapping)
