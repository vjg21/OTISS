import { useEffect, useState } from "react";
import { fetchDashboardStats } from "../../api/dashboardApi";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar, Doughnut } from "react-chartjs-2";
import "./Dashboard.css";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Tooltip,
  Legend
);

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardStats()
      .then((data) => setStats(data))
      .catch((err) => setError(err.message));
  }, []);

  if (error) {
    return <div className="dashboard-page">Error: {error}</div>;
  }

  if (!stats) {
    return <div className="dashboard-page">Loading dashboard...</div>;
  }

  /* ===== Indicator Composition Chart ===== */
  const indicatorChartData = {
    labels: ["Malicious IPs", "Malicious URLs", "Malware Hashes"],
    datasets: [
      {
        label: "Indicators",
        data: [
          stats.malicious_ips,
          stats.malicious_urls,
          stats.hashes,
        ],
        backgroundColor: ["#7f1d1d", "#991b1b", "#b91c1c"],
      },
    ],
  };

  const horizontalBarOptions = {
    indexAxis: "y",
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
    },
  };

  /* ===== Threat Feeds Chart ===== */
  const feedsChartData = {
    labels: stats.feeds,
    datasets: [
      {
        label: "Enabled Feeds",
        data: stats.feeds.map(() => 1),
        backgroundColor: ["#7f1d1d", "#991b1b", "#b91c1c"],
      },
    ],
  };

  const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "bottom",
      },
    },
  };

  return (
    <div className="dashboard-page">
     

      {/* ===== STAT CARDS ===== */}
      <div className="stats-grid">
        <div className="stat-card">
          <span>Indicators Analyzed</span>
          <h2>{stats.total_indicators}</h2>
        </div>

        <div className="stat-card">
          <span>High Risk IOCs</span>
          <h2>{stats.high_risk}</h2>
        </div>

        <div className="stat-card">
          <span>Malicious URLs</span>
          <h2>{stats.malicious_urls}</h2>
        </div>

        <div className="stat-card">
          <span>Malicious IPs</span>
          <h2>{stats.malicious_ips}</h2>
        </div>

        <div className="stat-card">
          <span>Malware Hashes</span>
          <h2>{stats.hashes}</h2>
        </div>

        <div className="stat-card">
          <span>Threat Feeds Enabled</span>
          <h2>{stats.feeds.length}</h2>
        </div>

        <div className="stat-card status">
          <span>System Status</span>
          <h2>{stats.status}</h2>
        </div>
      </div>

      {/* ===== CHARTS ===== */}
      <div className="charts-grid">
        <div className="chart-card">
          <h3>Indicator Composition</h3>
          <div className="chart-container">
            <Bar
              data={indicatorChartData}
              options={horizontalBarOptions}
            />
          </div>
        </div>

        <div className="chart-card">
          <h3>Enabled Threat Feeds</h3>
          <div className="chart-container">
            <Doughnut
              data={feedsChartData}
              options={doughnutOptions}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
