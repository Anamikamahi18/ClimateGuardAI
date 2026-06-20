import joblib

heatwave_features = joblib.load("models/heatwave_feature_names.pkl")

print("Heatwave Feature Count:", len(heatwave_features))

print(heatwave_features[:20])
