import { useState, useEffect } from "react";
import SearchBar from "../components/SearchBar";
import { getCompleteAnalysis } from "../api/climateApi";

function AnomalyDetection() {
  const [loading, setLoading] = useState(false);
  const [anomalyStatus, setAnomalyStatus] = useState(null);
  const [error, setError] = useState(null);

  const fetchAnomaly = async (city) => {
    try {
      setLoading(true);
      setError(null);
      const data = await getCompleteAnalysis(city);
      setAnomalyStatus(data.anomaly_status);
    } catch (err) {
      console.error("Error:", err);
      setError(`Unable to load anomaly information for ${city}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnomaly("Kochi");
  }, []);

  const isAnomaly = anomalyStatus === "Anomaly";

  return (
    <div className="page">
      <h1>🔍 Climate Anomaly Monitoring</h1>
      <SearchBar onSearch={fetchAnomaly} />

      {error && <div className="error-box">⚠️ {error}</div>}

      {loading && <div className="loading">⏳ Loading...</div>}

      {!loading && anomalyStatus && (
        <>
          <div className="anomaly-card">
            <h2>Current Status</h2>
            <div
              className="status-badge"
              style={{
                background: isAnomaly ? "#ef4444" : "#22c55e",
              }}
            >
              {isAnomaly ? "🔴 Anomaly Detected" : "🟢 Normal"}
            </div>
            <p style={{ marginTop: "15px", color: "#475569" }}>
              {isAnomaly
                ? "Environmental conditions differ significantly from historical patterns."
                : "Current environmental conditions are within expected operating ranges."}
            </p>
          </div>

          <div className="risk-panel">
            <h2>Risk Indicator</h2>
            <div className="risk-bar">
              <div
                className="risk-fill"
                style={{
                  width: isAnomaly ? "90%" : "25%",
                  background: isAnomaly
                    ? "linear-gradient(90deg, #ef4444, #dc2626)"
                    : "linear-gradient(90deg, #22c55e, #16a34a)",
                }}
              />
            </div>
            <h3 style={{ color: isAnomaly ? "#ef4444" : "#22c55e" }}>
              {isAnomaly ? "⚠️ High Risk" : "✅ Low Risk"}
            </h3>
          </div>

          <div className="anomaly-card">
            <h2>Monitoring Explanation</h2>
            {isAnomaly ? (
              <>
                <p>Isolation Forest detected an unusual environmental pattern.</p>
                <ul style={{ marginTop: "15px", marginLeft: "20px", color: "#475569" }}>
                  <li>Weather conditions may differ from historical observations</li>
                  <li>Air quality indicators may be abnormal</li>
                  <li>Climate risk should be monitored closely</li>
                </ul>
              </>
            ) : (
              <>
                <p>Environmental conditions appear normal.</p>
                <ul style={{ marginTop: "15px", marginLeft: "20px", color: "#475569" }}>
                  <li>Weather patterns are within expected ranges</li>
                  <li>Air quality indicators remain stable</li>
                  <li>No unusual climate behaviour detected</li>
                </ul>
              </>
            )}
          </div>

          <div className="anomaly-card">
            <h2>📊 Climate Monitoring Dashboard</h2>
            <div className="monitor-grid">
              <div className="monitor-tile">📡 Weather Monitoring</div>
              <div className="monitor-tile">💨 Air Quality Monitoring</div>
              <div className="monitor-tile">⚠️ Climate Risk Tracking</div>
              <div className="monitor-tile">🔍 Anomaly Surveillance</div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default AnomalyDetection;