from backend.services.model_loader import (
    rainfall_model,
    rainfall_mapping,
)

from backend.preprocessing.inference_pipeline import (
    build_rainfall_features,
    align_rainfall_features,
)


def predict_rainfall_risk_from_features(
    weather,
    air,
    location,
):

    features = build_rainfall_features(
        weather,
        air,
        location,
    )

    X = align_rainfall_features(features)

    prediction = rainfall_model.predict(X)[0]

    risk = rainfall_mapping[prediction]

    return {
        "rainfall_risk": risk,
        "features": features,
        "X": X,
    }
