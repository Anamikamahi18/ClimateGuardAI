import { useEffect, useState } from "react";
import SearchBar from "../components/SearchBar";
import RiskCard from "../components/RiskCard";
import { getCompleteAnalysis } from "../api/climateApi";

function Dashboard() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const fetchAnalysis = async (city) => {
    try {
      setLoading(true);
      setError(null);
      const result = await getCompleteAnalysis(city);
      setData(result);
    } catch (err) {
      console.error("Analysis Error:", err);
      setError(`Unable to fetch analysis for ${city}. Please check your backend.`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalysis("Kochi");
  }, []);

  return (
    <div className="page">
      <h1>🌍 ClimateGuard AI Dashboard</h1>

      <SearchBar onSearch={fetchAnalysis} />

      {error && (
        <div className="error-box">
          ⚠️ {error}
        </div>
      )}

      {loading && (
        <div className="loading">
          ⏳ Loading climate analysis...
        </div>
      )}

      {!loading && data && (
        <>
          <h2>📍 {data.city}</h2>

          <div className="card-grid">
            <RiskCard
              title="🌧️ Rainfall Risk"
              value={data.rainfall?.prediction || "N/A"}
              confidence={data.rainfall?.confidence || 0}
            />

            <RiskCard
              title="🔥 Heatwave Risk"
              value={data.heatwave?.prediction || "N/A"}
              confidence={data.heatwave?.confidence || 0}
            />

            <RiskCard
              title="⚠️ Climate Risk"
              value={data.climate_risk?.category || "N/A"}
            />

            <RiskCard
              title="🌐 Climate Profile"
              value={data.climate_profile || "N/A"}
            />

            <RiskCard
              title="🔍 Anomaly Status"
              value={data.anomaly_status || "N/A"}
            />
          </div>

          <div className="summary-box">
            <h3>📌 Location Details</h3>
            <p>
              <strong>Latitude:</strong> {data.coordinates?.latitude?.toFixed(4)}
            </p>
            <p>
              <strong>Longitude:</strong> {data.coordinates?.longitude?.toFixed(4)}
            </p>
          </div>
        </>
      )}
    </div>
  );
}

export default Dashboard;