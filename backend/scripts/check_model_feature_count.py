import joblib

model = joblib.load("models/xgboost_heatwave_model.pkl")
print(model.n_features_in_)
