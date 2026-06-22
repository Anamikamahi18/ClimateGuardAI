import { Link } from "react-router-dom";

function Sidebar() {

  return (

    <aside className="sidebar">

      <h2>
        ClimateGuard AI
      </h2>

      <ul>

        <li>
          <Link to="/">
            Dashboard
          </Link>
        </li>

        <li>
          <Link to="/explainability">
            Explainability
          </Link>
        </li>

        <li>
          <Link to="/climate-profile">
            Climate Profile
          </Link>
        </li>

        <li>
          <Link to="/anomaly-detection">
            Anomaly Detection
          </Link>
        </li>

      </ul>

    </aside>

  );
}

export default Sidebar;
