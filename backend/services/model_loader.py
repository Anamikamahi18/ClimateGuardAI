import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

MODELS_DIR = BASE_DIR / "models"


# ==================================================
# RAINFALL
# ==================================================

rainfall_model = joblib.load(MODELS_DIR / "xgboost_rainfall_model.pkl")

rainfall_features = joblib.load(MODELS_DIR / "rainfall_feature_names.pkl")

rainfall_mapping = joblib.load(MODELS_DIR / "rainfall_class_mapping.pkl")


# ==================================================
# HEATWAVE
# ==================================================

heatwave_model = joblib.load(MODELS_DIR / "xgboost_heatwave_model.pkl")

heatwave_features = joblib.load(MODELS_DIR / "heatwave_feature_names.pkl")

heatwave_encoder = joblib.load(MODELS_DIR / "heatwave_label_encoder.pkl")


# ==================================================
# CLIMATE PROFILE
# ==================================================

kmeans_model = joblib.load(MODELS_DIR / "kmeans_climate_profile.pkl")

clustering_scaler = joblib.load(MODELS_DIR / "clustering_scaler.pkl")

# ==================================================
# ANOMALY DETECTION
# ==================================================

isolation_forest = joblib.load(MODELS_DIR / "isolation_forest.pkl")

anomaly_scaler = joblib.load(MODELS_DIR / "anomaly_scaler.pkl")

print("All ClimateGuard AI models loaded successfully")
