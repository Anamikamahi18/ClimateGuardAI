import joblib
import shap
import numpy as np

from pathlib import Path

# ==================================================
# PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parents[2]
MODELS_DIR = BASE_DIR / "models"

# ==================================================
# LOAD MODELS
# ==================================================

rainfall_model = joblib.load(MODELS_DIR / "xgboost_rainfall_model.pkl")

heatwave_model = joblib.load(MODELS_DIR / "xgboost_heatwave_model.pkl")

rainfall_mapping = joblib.load(MODELS_DIR / "rainfall_class_mapping.pkl")

heatwave_encoder = joblib.load(MODELS_DIR / "heatwave_label_encoder.pkl")

# ==================================================
# SHAP EXPLAINERS
# ==================================================

rainfall_explainer = shap.TreeExplainer(rainfall_model)

heatwave_explainer = shap.TreeExplainer(heatwave_model)

# ==================================================
# EXCLUDED FEATURES
# ==================================================

EXCLUDED_FEATURES = {
    "latitude",
    "longitude",
    "year",
    "month",
    "day",
    "hour",
    "weekday",
    "moon_illumination",
    "day_period_1",
    "day_period_2",
    "season_1",
    "season_2",
    "season_3",
    "timezone_1",
    "timezone_2",
}

# ==================================================
# DISPLAY NAMES
# ==================================================

FEATURE_DISPLAY_NAMES = {
    "cloud": "Cloud Cover",
    "humidity": "Humidity",
    "visibility_km": "Visibility",
    "temperature_celsius": "Temperature",
    "pressure_mb": "Pressure",
    "uv_index": "UV Index",
    "air_quality_PM2.5": "PM2.5",
    "air_quality_PM10": "PM10",
    "air_quality_Carbon_Monoxide": "CO",
    "air_quality_Ozone": "Ozone",
    "air_quality_Nitrogen_dioxide": "NO₂",
    "air_quality_Sulphur_dioxide": "SO₂",
    "temperature_gap": "Temperature Gap",
    "heatwave_index": "Heatwave Index",
    "wind_humidity_interaction": "Wind-Humidity Interaction",
    "humidity_cloud_interaction": "Humidity-Cloud Interaction",
    "pollution_intensity": "Pollution Intensity",
    "pm_difference": "PM Difference",
}

# ==================================================
# RECOMMENDATIONS
# ==================================================

RAINFALL_RECOMMENDATIONS = {
    "Low": ["Normal outdoor activities are safe."],
    "Medium": ["Monitor rainfall forecasts.", "Carry rain protection."],
    "High": [
        "Avoid flood-prone areas.",
        "Monitor local weather alerts.",
        "Carry emergency supplies.",
    ],
}

HEATWAVE_RECOMMENDATIONS = {
    "Safe": ["Normal outdoor activities are safe."],
    "Warning": ["Stay hydrated.", "Avoid prolonged outdoor exposure."],
    "Critical": [
        "Avoid direct sunlight.",
        "Stay indoors during peak hours.",
        "Monitor vulnerable populations.",
    ],
}

# ==================================================
# HELPERS
# ==================================================


def impact_strength(shap_value):

    value = abs(shap_value)

    if value > 1:
        return "Very High"

    elif value > 0.5:
        return "High"

    elif value > 0.1:
        return "Medium"

    return "Low"


def generate_summary(prediction, drivers):

    if len(drivers) == 0:

        return f"Prediction is {prediction}."

    top_features = [x["display_name"] for x in drivers[:3]]

    return (
        f"Prediction is {prediction} "
        f"mainly due to {', '.join(top_features)}."
    )


def build_explanation(X, shap_values, prediction):

    risk_drivers = []
    risk_reducers = []

    for feature in X.columns:

        if feature in EXCLUDED_FEATURES:
            continue

        shap_value = float(shap_values[feature])

        explanation = {
            "feature": feature,
            "display_name": FEATURE_DISPLAY_NAMES.get(feature, feature),
            "feature_value": float(X.iloc[0][feature]),
            "impact": float(
                round(
                    float(shap_value),
                    4
                    )
                    ),

            "strength": impact_strength(shap_value),
        }

        if shap_value > 0:

            risk_drivers.append(explanation)

        else:

            risk_reducers.append(explanation)

    risk_drivers = sorted(
        risk_drivers,
        key=lambda x: abs(x["impact"]),
        reverse=True,
    )

    risk_reducers = sorted(
        risk_reducers,
        key=lambda x: abs(x["impact"]),
        reverse=True,
    )

    summary = generate_summary(prediction, risk_drivers)

    return (summary, risk_drivers[:10], risk_reducers[:10])


# ==================================================
# RAINFALL
# ==================================================


def explain_rainfall_prediction(X):

    prediction_id = int(rainfall_model.predict(X)[0])

    prediction = str(rainfall_mapping[prediction_id])

    probabilities = rainfall_model.predict_proba(X)[0]

    confidence = float(
        round(
            float(np.max(probabilities)) * 100,
            2
            )
            )

    shap_values = rainfall_explainer.shap_values(X)

    predicted_shap = (
        get_predicted_class_shap(
            shap_values,
            prediction_id
            )
            )

    print("Prediction:", prediction)
    print("Prediction ID:", prediction_id)
    print("SHAP Shape:", np.array(shap_values).shape)

    shap_dict = dict(zip(X.columns, predicted_shap))

    print(type(shap_values))
    print(shap_values)
    print(shap_values.shape)

    summary, drivers, reducers = build_explanation(X, shap_dict, prediction)

    result = {
        "prediction": prediction,
        "confidence": confidence,
        "summary": summary,
        "risk_drivers": drivers,
        "risk_reducers": reducers,
        "recommendations": RAINFALL_RECOMMENDATIONS.get(prediction, []),
    }
    
    print(type(confidence))
    print(type(prediction))

    return result


# ==================================================
# HEATWAVE
# ==================================================


def explain_heatwave_prediction(X):

    prediction_id = int(heatwave_model.predict(X)[0])

    prediction = str(heatwave_encoder.inverse_transform([prediction_id])[0])

    probabilities = heatwave_model.predict_proba(X)[0]

    confidence = float(
        round(
            float(np.max(probabilities)) * 100,
            2
            )
            )

    shap_values = heatwave_explainer.shap_values(X)

    predicted_shap = (
        get_predicted_class_shap(
            shap_values,
            prediction_id
        )
        )

    print("Prediction:", prediction)
    print("Prediction ID:", prediction_id)
    print("SHAP Shape:", np.array(shap_values).shape)
    shap_dict = dict(zip(X.columns, predicted_shap))

    summary, drivers, reducers = build_explanation(X, shap_dict, prediction)

    result = {
        "prediction": prediction,
        "confidence": confidence,
        "summary": summary,
        "risk_drivers": drivers,
        "risk_reducers": reducers,
        "recommendations": HEATWAVE_RECOMMENDATIONS.get(prediction, []),
    }
    
    print(type(confidence))
    print(type(prediction))

    return result


def get_predicted_class_shap(shap_values, prediction_id):
    """
    Supports:
    SHAP < 0.45
    SHAP 0.45+
    Binary
    Multiclass
    """

    # old format
    if isinstance(shap_values, list):

        return shap_values[prediction_id][0]

    # new ndarray format

    if isinstance(shap_values, np.ndarray):

        if len(shap_values.shape) == 3:

            # (samples, features, classes)

            return shap_values[0, :, prediction_id]

        elif len(shap_values.shape) == 2:

            # binary

            return shap_values[0]

    raise ValueError(f"Unsupported SHAP shape: " f"{shap_values.shape}")
