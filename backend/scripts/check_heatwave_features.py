import joblib

features = joblib.load("models/heatwave_feature_names.pkl")
for i, f in enumerate(features):
    print(i, repr(f))
features[-15:]
