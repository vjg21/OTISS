import { useLocation, Link } from "react-router-dom";
import { useEffect, useState } from "react";
import {
  FiHome,
  FiSearch,
  FiAlertTriangle,
  FiTool,
  FiInfo,
  FiHelpCircle,
  FiChevronRight,
  FiMoon,
  FiSun
} from "react-icons/fi";
import "./Topbar.css";

const pageMeta = {
  "/": { title: "Dashboard", subtitle: "Real-time threat intelligence overview", icon: <FiHome /> },
  "/analyze": { title: "Analyze", subtitle: "Analyze indicators using multiple intelligence sources", icon: <FiSearch /> },
  "/vulnerabilities": { title: "Vulnerabilities", subtitle: "Track and assess known security vulnerabilities", icon: <FiAlertTriangle /> },
  "/tools": { title: "Tools", subtitle: "Curated external threat intelligence and security tools", icon: <FiTool /> },
  "/about": { title: "About", subtitle: "Information about the OTISS platform", icon: <FiInfo /> },
  "/help": { title: "Help", subtitle: "Usage guide and analyst best practices", icon: <FiHelpCircle /> }
};

export default function Topbar() {
  const location = useLocation();
  const meta = pageMeta[location.pathname] || pageMeta["/"];

  const [darkMode, setDarkMode] = useState(
    localStorage.getItem("theme") === "dark"
  );

  useEffect(() => {
    document.body.classList.toggle("dark", darkMode);
    localStorage.setItem("theme", darkMode ? "dark" : "light");
  }, [darkMode]);

  return (
    <header className="topbar">
      <div className="topbar-text">
        <h1>{meta.title}</h1>
        <p>{meta.subtitle}</p>

        {/* BREADCRUMB */}
        <div className="breadcrumb">
          <Link to="/" className="crumb">
            <FiHome /> Home
          </Link>
          <FiChevronRight className="sep" />
          <span className="crumb current">
            {meta.icon} {meta.title}
          </span>
        </div>
      </div>

      {/* DARK MODE TOGGLE */}
     
    </header>
  );
}
