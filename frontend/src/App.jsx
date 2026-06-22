import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import Navbar from "./components/Navbar";

import Dashboard from "./pages/Dashboard";
import Explainability from "./pages/Explainability";
import ClimateProfile from "./pages/ClimateProfile";
import AnomalyDetection from "./pages/AnomalyDetection";

function App() {
  return (
    <BrowserRouter>

      <Navbar />

      <Routes>

        <Route
          path="/"
          element={<Dashboard />}
        />

        <Route
          path="/explainability"
          element={<Explainability />}
        />

        <Route
          path="/climate-profile"
          element={<ClimateProfile />}
        />

        <Route
          path="/anomaly"
          element={<AnomalyDetection />}
        />

      </Routes>

    </BrowserRouter>
  );
}

export default App;
