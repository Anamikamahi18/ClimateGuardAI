from backend.preprocessing.inference_pipeline import build_rainfall_features


def build_features(weather_data, air_quality_data, location_data):

    features = build_rainfall_features(
        weather_data, air_quality_data, location_data
    )

    features.setdefault("precip_mm", 0)

    features.setdefault(
        "temperature_gap",
        features.get("feels_like_celsius", 0)
        - features.get("temperature_celsius", 0),
    )

    return features
