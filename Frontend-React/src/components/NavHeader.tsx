import { NavLink } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="navbar navbar-expand-lg bg-dark-subtle">
      <NavLink to="/" className="navbar-brand">
        Home
      </NavLink>
      <ul className="navbar-nav me-auto mb-2 mb-lg-0">
        <li className="nav-item">
          <NavLink to="/Dungeons" className="nav-link">
            Dungeons
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/about" className="nav-link">
            about
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/new-entry" className="nav-link">
            New Entry
          </NavLink>
        </li>
      </ul>
    </nav>
  );
}
