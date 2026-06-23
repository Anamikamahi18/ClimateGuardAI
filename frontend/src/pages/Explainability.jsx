import { useState } from "react";

import SearchBar from "../components/SearchBar";
import DriverTable from "../components/DriverTable";

import {
  getCompleteAnalysis,
} from "../api/climateApi";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function Explainability() {

  const [loading, setLoading] =
    useState(false);

  const [rainfallDrivers, setRainfallDrivers] =
    useState([]);

  const [heatwaveDrivers, setHeatwaveDrivers] =
    useState([]);

  const fetchData = async (city) => {

    try {

      setLoading(true);

      const data =
        await getCompleteAnalysis(city);

      setRainfallDrivers(
        data.explanations
          .rainfall
          .risk_drivers
      );

      setHeatwaveDrivers(
        data.explanations
          .heatwave
          .risk_drivers
      );

    } catch (error) {

      console.error(error);

      alert(
        "Unable to load explainability."
      );

    } finally {

      setLoading(false);

    }
  };

  return (
    <div className="page">

      <h1>
        Explainability Dashboard
      </h1>

      <SearchBar
        onSearch={fetchData}
      />

      {loading && (
        <h3>Loading...</h3>
      )}

      {!loading &&
        rainfallDrivers.length > 0 && (
        <>

          {/* ======================= */}
          {/* Rainfall Drivers */}
          {/* ======================= */}

          <section>

            <h2>
              Top Rainfall Drivers
            </h2>

            <ol>
              {rainfallDrivers
                .slice(0, 5)
                .map((item) => (
                  <li
                    key={item.feature}
                  >
                    {
                      item.display_name
                    }
                  </li>
                ))}
            </ol>

            <div
              style={{
                width: "100%",
                height: 350,
              }}
            >
              <ResponsiveContainer>

                <BarChart
                  data={
                    rainfallDrivers
                      .slice(0, 5)
                  }
                >

                  <XAxis
                    dataKey="display_name"
                  />

                  <YAxis />

                  <Tooltip />

                  <Bar
                    dataKey="impact"
                  />

                </BarChart>

              </ResponsiveContainer>
            </div>

            <DriverTable
              title="Rainfall Driver Details"
              drivers={
                rainfallDrivers
              }
            />

          </section>

          {/* ======================= */}
          {/* Heatwave Drivers */}
          {/* ======================= */}

          <section
            style={{
              marginTop: 40,
            }}
          >

            <h2>
              Top Heatwave Drivers
            </h2>

            <ol>
              {heatwaveDrivers
                .slice(0, 5)
                .map((item) => (
                  <li
                    key={item.feature}
                  >
                    {
                      item.display_name
                    }
                  </li>
                ))}
            </ol>

            <div
              style={{
                width: "100%",
                height: 350,
              }}
            >
              <ResponsiveContainer>

                <BarChart
                  data={
                    heatwaveDrivers
                      .slice(0, 5)
                  }
                >

                  <XAxis
                    dataKey="display_name"
                  />

                  <YAxis />

                  <Tooltip />

                  <Bar
                    dataKey="impact"
                  />

                </BarChart>

              </ResponsiveContainer>
            </div>

            <DriverTable
              title="Heatwave Driver Details"
              drivers={
                heatwaveDrivers
              }
            />

          </section>

        </>
      )}

    </div>
  );
}

export default Explainability;
