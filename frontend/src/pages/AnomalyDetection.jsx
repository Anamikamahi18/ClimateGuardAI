import { useState } from "react";

import SearchBar from "../components/SearchBar";

import {
  getCompleteAnalysis,
} from "../api/climateApi";

function AnomalyDetection() {

  const [loading, setLoading] =
    useState(false);

  const [anomalyStatus, setAnomalyStatus] =
    useState(null);

  const fetchAnomaly = async (city) => {

    try {

      setLoading(true);

      const data =
        await getCompleteAnalysis(city);

      setAnomalyStatus(
        data.anomaly_status
      );

    } catch (error) {

      console.error(error);

      alert(
        "Unable to load anomaly information."
      );

    } finally {

      setLoading(false);

    }
  };

  const isAnomaly =
    anomalyStatus === "Anomaly";

  return (

    <div className="page">

      <h1>
        Climate Anomaly Monitoring
      </h1>

      <SearchBar
        onSearch={fetchAnomaly}
      />

      {loading && (
        <h3>Loading...</h3>
      )}

      {!loading &&
        anomalyStatus && (

        <>
          {/* Status Card */}

          <div
            className="anomaly-card"
          >

            <h2>
              Current Status
            </h2>

            <div
              className="status-badge"
              style={{
                background:
                  isAnomaly
                    ? "#ef4444"
                    : "#22c55e",
              }}
            >
              {anomalyStatus}
            </div>

            <p>

              {
                isAnomaly
                  ? "Environmental conditions differ significantly from historical patterns."
                  : "Current environmental conditions are within expected operating ranges."
              }

            </p>

          </div>

          {/* Risk Indicator */}

          <div
            className="risk-panel"
          >

            <h2>
              Risk Indicator
            </h2>

            <div
              className="risk-bar"
            >

              <div
                className="risk-fill"
                style={{
                  width:
                    isAnomaly
                      ? "90%"
                      : "25%",

                  background:
                    isAnomaly
                      ? "#ef4444"
                      : "#22c55e",
                }}
              />

            </div>

            <h3>

              {
                isAnomaly
                  ? "High Risk"
                  : "Low Risk"
              }

            </h3>

          </div>

          {/* Explanation */}

          <div
            className="anomaly-card"
          >

            <h2>
              Monitoring Explanation
            </h2>

            {
              isAnomaly
              ? (
                <>
                  <p>
                    Isolation Forest detected
                    an unusual environmental
                    pattern.
                  </p>

                  <ul>
                    <li>
                      Weather conditions may
                      differ significantly from
                      historical observations.
                    </li>

                    <li>
                      Air quality indicators
                      may be abnormal.
                    </li>

                    <li>
                      Climate risk should be
                      monitored closely.
                    </li>
                  </ul>
                </>
              )
              : (
                <>
                  <p>
                    Environmental conditions
                    appear normal.
                  </p>

                  <ul>
                    <li>
                      Weather patterns are
                      within expected ranges.
                    </li>

                    <li>
                      Air quality indicators
                      remain stable.
                    </li>

                    <li>
                      No unusual climate
                      behaviour detected.
                    </li>
                  </ul>
                </>
              )
            }

          </div>

          {/* Monitoring Dashboard */}

          <div
            className="anomaly-card"
          >

            <h2>
              Climate Monitoring Dashboard
            </h2>

            <div
              className="monitor-grid"
            >

              <div
                className="monitor-tile"
              >
                Weather Monitoring
              </div>

              <div
                className="monitor-tile"
              >
                Air Quality Monitoring
              </div>

              <div
                className="monitor-tile"
              >
                Climate Risk Tracking
              </div>

              <div
                className="monitor-tile"
              >
                Anomaly Surveillance
              </div>

            </div>

          </div>

        </>
      )}

    </div>
  );
}

export default AnomalyDetection;
