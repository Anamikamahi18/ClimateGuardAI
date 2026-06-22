import {
  Link,
} from "react-router-dom";

function Navbar() {
  return (
    <nav className="navbar">
      <Link to="/">
        Dashboard
      </Link>

      <Link to="/explainability">
        Explainability
      </Link>

      <Link to="/climate-profile">
        Climate Profile
      </Link>

      <Link to="/anomaly">
        Anomaly Detection
      </Link>
    </nav>
  );
}

export default Navbar;
