import pandas as pd


def build_common_features(
    weather_data,
    air_quality_data,
    location_data
):
    """
    Build common features shared by
    rainfall and heatwave models.
    """

    features = {}

    return features


def build_rainfall_features(
    weather_data,
    air_quality_data,
    location_data
):
    """
    Rainfall Model
    94 Features
    """

    features = build_common_features(
        weather_data,
        air_quality_data,
        location_data
    )

    return pd.DataFrame([features])


def build_heatwave_features(
    weather_data,
    air_quality_data,
    location_data
):
    """
    Heatwave Model
    93 Features
    """

    features = build_common_features(
        weather_data,
        air_quality_data,
        location_data
    )

    return pd.DataFrame([features])
