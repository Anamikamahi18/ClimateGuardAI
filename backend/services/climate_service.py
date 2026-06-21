RAINFALL_SCORES = {"Low": 10, "Medium": 40, "High": 80}

HEATWAVE_SCORES = {"Safe": 10, "Warning": 50, "Critical": 90}

ANOMALY_SCORES = {"Normal": 0, "Anomaly": 100}

PROFILE_SCORES = {
    "Moderate": 20,
    "Pollution-Prone": 50,
    "Flood-Prone": 70,
    "Extreme-Pollution": 90,
}


def calculate_climate_risk(
    rainfall_risk: str,
    heatwave_risk: str,
    anomaly_status: str,
    climate_profile: str,
):

    rainfall_score = RAINFALL_SCORES[rainfall_risk]

    heatwave_score = HEATWAVE_SCORES[heatwave_risk]

    anomaly_score = ANOMALY_SCORES[anomaly_status]

    profile_score = PROFILE_SCORES[climate_profile]

    final_score = (
        0.30 * rainfall_score
        + 0.30 * heatwave_score
        + 0.20 * profile_score
        + 0.20 * anomaly_score
    )

    final_score = round(final_score)

    if final_score < 30:
        category = "Low"

    elif final_score < 60:
        category = "Moderate"

    elif final_score < 80:
        category = "High"

    else:
        category = "Severe"

    return {"climate_risk_score": final_score, "climate_risk": category}
