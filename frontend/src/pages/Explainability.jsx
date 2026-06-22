import { useState, useEffect } from "react";
import SearchBar from "../components/SearchBar";
import DriverTable from "../components/DriverTable";
import { getCompleteAnalysis } from "../api/climateApi";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function Explainability() {
  const [loading, setLoading] = useState(false);
  const [rainfallDrivers, setRainfallDrivers] = useState([]);
  const [heatwaveDrivers, setHeatwaveDrivers] = useState([]);
  const [error, setError] = useState(null);

  const fetchData = async (city) => {
    try {
      setLoading(true);
      setError(null);
      const data = await getCompleteAnalysis(city);
      setRainfallDrivers(data.explanations?.rainfall?.risk_drivers || []);
      setHeatwaveDrivers(data.explanations?.heatwave?.risk_drivers || []);
    } catch (err) {
      console.error("Error:", err);
      setError(`Unable to load explainability for ${city}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData("Kochi");
  }, []);

  return (
    <div className="page">
      <h1>📊 Explainability Dashboard</h1>
      <SearchBar onSearch={fetchData} />

      {error && <div className="error-box">⚠️ {error}</div>}

      {loading && <div className="loading">⏳ Loading...</div>}

      {!loading && rainfallDrivers.length > 0 && (
        <>
          <section>
            <h2>🌧️ Top Rainfall Risk Drivers</h2>
            <ol>
              {rainfallDrivers.slice(0, 5).map((item) => (
                <li key={item.feature}>{item.display_name}</li>
              ))}
            </ol>
            <div style={{ width: "100%", height: 350, marginTop: "20px" }}>
              <ResponsiveContainer>
                <BarChart data={rainfallDrivers.slice(0, 5)}>
                  <XAxis dataKey="display_name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="impact" fill="#3b82f6" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
            <DriverTable
              title="Rainfall Driver Details"
              drivers={rainfallDrivers}
            />
          </section>

          <section>
            <h2>🔥 Top Heatwave Risk Drivers</h2>
            <ol>
              {heatwaveDrivers.slice(0, 5).map((item) => (
                <li key={item.feature}>{item.display_name}</li>
              ))}
            </ol>
            <div style={{ width: "100%", height: 350, marginTop: "20px" }}>
              <ResponsiveContainer>
                <BarChart data={heatwaveDrivers.slice(0, 5)}>
                  <XAxis dataKey="display_name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="impact" fill="#f59e0b" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
            <DriverTable
              title="Heatwave Driver Details"
              drivers={heatwaveDrivers}
            />
          </section>
        </>
      )}
    </div>
  );
}

export default Explainability;