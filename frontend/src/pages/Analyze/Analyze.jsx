import { useState } from "react";
import { analyzeUnified, analyzeBulk } from "../../api/analyzeApi";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";
import "./Analyze.css";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
);

/* =========================
   IOC VALIDATION (FIXED)
========================= */
const ipRegex =
  /^(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)$/;

const cidrRegex =
  /^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)\/([0-9]|[1-2][0-9]|3[0-2])$/;

const domainRegex =
  /^(?!:\/\/)([a-zA-Z0-9-_]+\.)+[a-zA-Z]{2,}$/;

const urlRegex =
  /^(https?:\/\/)([\w\-]+\.)+[a-z]{2,}(\/\S*)?$/i;

const hashRegex =
  /^[A-Fa-f0-9]{32}$|^[A-Fa-f0-9]{40}$|^[A-Fa-f0-9]{64}$/;

function isValidIOC(v) {
  return (
    ipRegex.test(v) ||
    cidrRegex.test(v) ||
    urlRegex.test(v) ||
    domainRegex.test(v) ||
    hashRegex.test(v)
  );
}

/* =========================
   TOOLS
========================= */
const TOOLS = [
  { key: "use_otx", label: "OTX" },
  { key: "use_virustotal", label: "VIRUSTOTAL" },
  { key: "use_urlscan", label: "URLSCAN" },
  { key: "use_securitytrails", label: "SECURITYTRAILS" },
  { key: "use_dns", label: "DNS" },
];

export default function Analyze() {
  const [mode, setMode] = useState("unified");
  const [input, setInput] = useState("");
  const [tools, setTools] = useState({});
  const [results, setResults] = useState([]);

  const toggleTool = (k) =>
    setTools((prev) => ({ ...prev, [k]: !prev[k] }));

  /* =========================
     ANALYZE HANDLER
  ========================= */
  const handleAnalyze = async () => {
    if (!input.trim()) return;

    /* -------- UNIFIED -------- */
    if (mode === "unified") {
      const indicator = input.trim();

      if (!isValidIOC(indicator)) {
        setResults([
          {
            indicator,
            type: "unknown",
            verdict: "INVALID",
            risk_level: "-",
            confidence: 0,
            sources: [],
          },
        ]);
        return;
      }

      const res = await analyzeUnified({
        indicator,
        ...tools,
      });

      setResults(res ? [res] : []);
    }

    /* -------- BULK -------- */
    else {
      const raw = input
        .split("\n")
        .map((i) => i.trim())
        .filter(Boolean);

      const valid = raw.filter(isValidIOC);
      const invalid = raw.filter((i) => !isValidIOC(i));

      let apiResults = [];

      if (valid.length > 0) {
        const res = await analyzeBulk({
          indicators: valid,
          ...tools,
        });

        if (Array.isArray(res)) apiResults = res;
        else if (Array.isArray(res?.results)) apiResults = res.results;
      }

      const invalidRows = invalid.map((v) => ({
        indicator: v,
        type: "unknown",
        verdict: "INVALID",
        risk_level: "-",
        confidence: 0,
        sources: [],
      }));

      setResults([...apiResults, ...invalidRows]);
    }
  };

  /* =========================
     SAFE RESULTS
  ========================= */
  const safeResults = Array.isArray(results) ? results : [];

  /* =========================
     RISK CHART
  ========================= */
  const riskCounts = safeResults.reduce(
    (acc, r) => {
      if (r.verdict === "INVALID") return acc;

      const risk = (r?.risk_level || "").toUpperCase();
      if (risk === "LOW") acc.low++;
      if (risk === "MEDIUM") acc.medium++;
      if (risk === "HIGH") acc.high++;
      return acc;
    },
    { low: 0, medium: 0, high: 0 }
  );

  const chartData = {
    labels: ["LOW", "MEDIUM", "HIGH"],
    datasets: [
      {
        data: [
          riskCounts.low,
          riskCounts.medium,
          riskCounts.high,
        ],
        backgroundColor: ["#16a34a", "#d97706", "#dc2626"],
      },
    ],
  };

  return (
    <div className="analyze-page">
      {/* ROW 1 */}
      <div className="analyze-grid">
        <div className="card input-card">
          <h3>Indicator Input</h3>

          <textarea
            placeholder="IP, CIDR, URL, domain, hash (one per line for bulk)"
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />

          <div className="mode-toggle">
            <button
              className={mode === "unified" ? "active" : ""}
              onClick={() => setMode("unified")}
            >
              Unified
            </button>
            <button
              className={mode === "bulk" ? "active" : ""}
              onClick={() => setMode("bulk")}
            >
              Bulk
            </button>
          </div>

          <div className="tool-buttons">
            {TOOLS.map((t) => (
              <button
                key={t.key}
                className={tools[t.key] ? "tool active" : "tool"}
                onClick={() => toggleTool(t.key)}
              >
                {t.label}
              </button>
            ))}
          </div>

          <div className="analyze-btn-wrapper">
            <button className="analyze-btn" onClick={handleAnalyze}>
              Analyze
            </button>
          </div>
        </div>

        <div className="card meaning-card">
          <h3>Report Field Meanings</h3>
          <p><strong>Benign</strong> – No malicious activity</p>
          <p><strong>Suspicious</strong> – Requires analyst review</p>
          <p><strong>Malicious</strong> – Confirmed threat</p>
          <p><strong>Invalid</strong> – Unsupported or malformed input</p>
        </div>
      </div>

      {/* ROW 2 */}
      {safeResults.length > 0 && (
        <div className="analyze-grid">
          <div className="card table-card">
            <h3>Analysis Results</h3>
            <table>
              <thead>
                <tr>
                  <th>Indicator</th>
                  <th>Type</th>
                  <th>Verdict</th>
                  <th>Risk</th>
                  <th>Confidence</th>
                  <th>Sources</th>
                </tr>
              </thead>
              <tbody>
                {safeResults.map((r, i) => (
                  <tr key={i}>
                    <td>{r.indicator}</td>
                    <td>{r.type}</td>
                    <td className={`verdict ${r.verdict?.toLowerCase()}`}>
                      {r.verdict}
                    </td>
                    <td>{r.risk_level}</td>
                    <td>
                      {r.verdict === "INVALID"
                        ? "-"
                        : Math.round((r.confidence || 0) * 100) + "%"}
                    </td>
                    <td>{r.sources?.join(", ") || "-"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="card chart-card">
            <h3>Risk Distribution</h3>
            <div className="chart-wrap">
              <Bar
                data={chartData}
                options={{
                  indexAxis: "y",
                  maintainAspectRatio: false,
                }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
