import joblib

features = joblib.load("models/heatwave_feature_names.pkl")

print("Feature Count:", len(features))

for i, feature in enumerate(features):
    print(i, feature)
