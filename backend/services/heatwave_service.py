from backend.services.model_loader import (
    heatwave_model,
    heatwave_encoder,
)

from backend.preprocessing.inference_pipeline import (
    build_heatwave_features,
    align_heatwave_features,
)


def predict_heatwave_from_features(
    weather,
    air,
    location,
):

    features = build_heatwave_features(
        weather,
        air,
        location,
    )

    X = align_heatwave_features(features)

    prediction = heatwave_model.predict(X)[0]

    risk = heatwave_encoder.inverse_transform([prediction])[0]

    return {
        "heatwave_risk": risk,
        "features": features,
        "X": X,
    }
