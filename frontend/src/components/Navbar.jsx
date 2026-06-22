import { Link } from "react-router-dom";

function Navbar() {

  return (

    <div className="navbar">

      <div className="brand">

        🌍 ClimateGuard AI

      </div>

      <div className="nav-links">

        <Link to="/">
          Dashboard
        </Link>

        <Link to="/explainability">
          Explainability
        </Link>

        <Link to="/climate-profile">
          Climate Profile
        </Link>

        <Link to="/anomaly-detection">
          Anomaly Detection
        </Link>

      </div>

    </div>

  );
}

export default Navbar;
