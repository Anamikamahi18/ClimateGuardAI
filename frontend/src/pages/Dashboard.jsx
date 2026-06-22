import { useEffect, useState } from "react";

import SearchBar from "../components/SearchBar";
import RiskCard from "../components/RiskCard";

import {
  getCompleteAnalysis,
} from "../api/climateApi";

function Dashboard() {

  const [loading, setLoading] =
    useState(false);

  const [data, setData] =
    useState(null);

  const fetchAnalysis = async (
    city
  ) => {

    try {

      setLoading(true);

      const result =
        await getCompleteAnalysis(city);

      setData(result);

    } catch (error) {

      console.error(
        "Analysis Error:",
        error
      );

      alert(
        "Unable to fetch climate analysis."
      );

    } finally {

      setLoading(false);

    }
  };

  useEffect(() => {

    fetchAnalysis("Kochi");

  }, []);

  return (
    <div className="page">

      <h1>
        ClimateGuard AI Dashboard
      </h1>

      <SearchBar
        onSearch={fetchAnalysis}
      />

      {loading && (
        <h3>Loading...</h3>
      )}

      {!loading && data && (

        <>

          <h2>
            {data.city}
          </h2>

          <div className="card-grid">

            <RiskCard
              title="Rainfall Risk"
              value={
                data.rainfall.prediction
              }
              confidence={
                data.rainfall.confidence
              }
            />

            <RiskCard
              title="Heatwave Risk"
              value={
                data.heatwave.prediction
              }
              confidence={
                data.heatwave.confidence
              }
            />

            <RiskCard
              title="Climate Risk"
              value={
                data.climate_risk.category
              }
            />

            <RiskCard
              title="Climate Profile"
              value={
                data.climate_profile
              }
            />

            <RiskCard
              title="Anomaly Status"
              value={
                data.anomaly_status
              }
            />

          </div>

          <div className="summary-box">

            <h3>
              Coordinates
            </h3>

            <p>
              Latitude:
              {" "}
              {
                data.coordinates.latitude
              }
            </p>

            <p>
              Longitude:
              {" "}
              {
                data.coordinates.longitude
              }
            </p>

          </div>

        </>

      )}

    </div>
  );
}

export default Dashboard;
