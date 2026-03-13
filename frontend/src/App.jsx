import { Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Topbar from "./components/Topbar";

import Dashboard from "./pages/Dashboard/Dashboard";
import Analyze from "./pages/Analyze/Analyze";
import Vulnerabilities from "./pages/Vulnerabilities/Vulnerabilities";
import Tools from "./pages/Tools/Tools";
import About from "./pages/About/About";
import Help from "./pages/Help/Help";

import "./App.css";

export default function App() {
  return (
    <div className="app-layout">
      {/* Sidebar */}
      <Sidebar />

      {/* Right side content */}
      <div className="content-area">
        {/* Topbar */}
        <Topbar />

        {/* Main page content */}
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/analyze" element={<Analyze />} />
            <Route path="/vulnerabilities" element={<Vulnerabilities />} />
            <Route path="/tools" element={<Tools />} />
            <Route path="/about" element={<About />} />
            <Route path="/help" element={<Help />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}
