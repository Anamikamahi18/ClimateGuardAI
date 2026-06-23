import { useState } from "react";

import SearchBar from "../components/SearchBar";

import {
  getCompleteAnalysis,
} from "../api/climateApi";

const PROFILE_CONFIG = {

  "Moderate": {
    color: "#22c55e",
    title: "Moderate",
    description:
      "Balanced environmental conditions with relatively low pollution levels and manageable climate risks.",
  },

  "Flood-Prone": {
    color: "#3b82f6",
    title: "Flood-Prone",
    description:
      "High humidity, cloud cover and rainfall conditions indicate elevated flood susceptibility.",
  },

  "Pollution-Prone": {
    color: "#f59e0b",
    title: "Pollution-Prone",
    description:
      "Air quality indicators suggest increased pollution concentration and environmental stress.",
  },

  "Extreme-Pollution": {
    color: "#ef4444",
    title: "Extreme Pollution",
    description:
      "Severe pollution levels detected with potentially harmful environmental conditions.",
  },

};

function ClimateProfile() {

  const [profile, setProfile] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const fetchProfile = async (city) => {

    try {

      setLoading(true);

      const data =
        await getCompleteAnalysis(city);

      setProfile(
        data.climate_profile
      );

    } catch (error) {

      console.error(error);

      alert(
        "Unable to load climate profile."
      );

    } finally {

      setLoading(false);

    }
  };

  const profileInfo =
    PROFILE_CONFIG[profile];

  return (

    <div className="page">

      <h1>
        Climate Profile Intelligence
      </h1>

      <SearchBar
        onSearch={fetchProfile}
      />

      {loading && (
        <h3>Loading...</h3>
      )}

      {!loading &&
        profile &&
        profileInfo && (

        <div
          className="profile-card"
          style={{
            borderLeft:
              `8px solid ${profileInfo.color}`,
          }}
        >

          <h2>
            Current Climate Profile
          </h2>

          <div
            className="profile-badge"
            style={{
              background:
                profileInfo.color,
            }}
          >
            {profileInfo.title}
          </div>

          <p>
            {profileInfo.description}
          </p>

        </div>
      )}

      {!loading && profile && (

        <div className="profiles-grid">

          {Object.entries(
            PROFILE_CONFIG
          ).map(
            ([key, value]) => (

              <div
                key={key}
                className="profile-tile"
                style={{
                  borderTop:
                    `6px solid ${value.color}`,
                }}
              >

                <h3>
                  {value.title}
                </h3>

                <p>
                  {value.description}
                </p>

              </div>
            )
          )}

        </div>
      )}

    </div>
  );
}

export default ClimateProfile;
