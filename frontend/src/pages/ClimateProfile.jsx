import { useState, useEffect } from "react";
import SearchBar from "../components/SearchBar";
import { getCompleteAnalysis } from "../api/climateApi";

const PROFILE_CONFIG = {
  Moderate: {
    color: "#22c55e",
    title: "🟢 Moderate",
    description:
      "Balanced environmental conditions with relatively low pollution levels and manageable climate risks.",
  },
  "Flood-Prone": {
    color: "#3b82f6",
    title: "🔵 Flood-Prone",
    description:
      "High humidity, cloud cover and rainfall conditions indicate elevated flood susceptibility.",
  },
  "Pollution-Prone": {
    color: "#f59e0b",
    title: "🟠 Pollution-Prone",
    description:
      "Air quality indicators suggest increased pollution concentration and environmental stress.",
  },
  "Extreme-Pollution": {
    color: "#ef4444",
    title: "🔴 Extreme Pollution",
    description:
      "Severe pollution levels detected with potentially harmful environmental conditions.",
  },
};

function ClimateProfile() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchProfile = async (city) => {
    try {
      setLoading(true);
      setError(null);
      const data = await getCompleteAnalysis(city);
      setProfile(data.climate_profile);
    } catch (err) {
      console.error("Error:", err);
      setError(`Unable to load climate profile for ${city}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfile("Kochi");
  }, []);

  const profileInfo = PROFILE_CONFIG[profile];

  return (
    <div className="page">
      <h1>🌍 Climate Profile Intelligence</h1>
      <SearchBar onSearch={fetchProfile} />

      {error && <div className="error-box">⚠️ {error}</div>}

      {loading && <div className="loading">⏳ Loading...</div>}

      {!loading && profile && profileInfo && (
        <div
          className="profile-card"
          style={{
            borderLeft: `6px solid ${profileInfo.color}`,
          }}
        >
          <h2>Current Climate Profile</h2>
          <div
            className="profile-badge"
            style={{ background: profileInfo.color }}
          >
            {profileInfo.title}
          </div>
          <p style={{ fontSize: "16px", color: "#475569", marginTop: "15px" }}>
            {profileInfo.description}
          </p>
        </div>
      )}

      {!loading && profile && (
        <div className="profiles-grid">
          {Object.entries(PROFILE_CONFIG).map(([key, value]) => (
            <div
              key={key}
              className="profile-tile"
              style={{
                borderTopColor: value.color,
              }}
            >
              <h3>{value.title}</h3>
              <p>{value.description}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ClimateProfile;