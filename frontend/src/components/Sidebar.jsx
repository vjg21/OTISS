import { NavLink } from "react-router-dom";
import { useState } from "react";
import {
  FiHome,
  FiSearch,
  FiAlertTriangle,
  FiTool,
  FiInfo,
  FiHelpCircle,
  FiChevronLeft,
  FiChevronRight,
  FiShield
} from "react-icons/fi";

import "./Sidebar.css";

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside className={`sidebar ${collapsed ? "collapsed" : ""}`}>
      {/* HEADER */}
      <div className="sidebar-header">
        {!collapsed && (
          <div className="brand">
            <FiShield className="brand-icon" />
            <span className="brand-text">OTISS</span>
          </div>
        )}

        <button
          className="collapse-btn"
          onClick={() => setCollapsed(!collapsed)}
          aria-label="Toggle sidebar"
        >
          {collapsed ? <FiChevronRight /> : <FiChevronLeft />}
        </button>
      </div>

      {/* NAV */}
      <nav className="sidebar-nav">
        <NavLink to="/" end>
          <FiHome />
          {!collapsed && <span>Dashboard</span>}
        </NavLink>

        <NavLink to="/analyze">
          <FiSearch />
          {!collapsed && <span>Analyze</span>}
        </NavLink>

        <NavLink to="/vulnerabilities">
          <FiAlertTriangle />
          {!collapsed && <span>Vulnerabilities</span>}
        </NavLink>

        <NavLink to="/tools">
          <FiTool />
          {!collapsed && <span>Tools</span>}
        </NavLink>

        <NavLink to="/about">
          <FiInfo />
          {!collapsed && <span>About</span>}
        </NavLink>

        <NavLink to="/help">
          <FiHelpCircle />
          {!collapsed && <span>Help</span>}
        </NavLink>
      </nav>
    </aside>
  );
}
