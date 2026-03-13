import { useState } from "react";
import "./Vulnerabilities.css";

const API_BASE = "http://127.0.0.1:8000";

export default function Vulnerabilities() {
  const [cve, setCve] = useState("");
  const [searchResult, setSearchResult] = useState([]);
  const [listResult, setListResult] = useState([]);
  const [activeSource, setActiveSource] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchCVE = async () => {
    if (!cve.trim()) return;
    setLoading(true);
    setActiveSource(null);
    setListResult([]);

    const res = await fetch(
      `${API_BASE}/vulnerabilities/cve/${cve.trim().toUpperCase()}`
    );
    const data = await res.json();
    setSearchResult(res.ok ? [data] : []);
    setLoading(false);
  };

  const fetchNVD = async () => {
    setLoading(true);
    setActiveSource("nvd");
    setSearchResult([]);

    const res = await fetch(`${API_BASE}/vulnerabilities/nvd`);
    const data = await res.json();
    setListResult(data);

    setLoading(false);
  };

  const fetchCISA = async () => {
    setLoading(true);
    setActiveSource("cisa");
    setSearchResult([]);

    const res = await fetch(`${API_BASE}/vulnerabilities/cisa-kev`);
    const data = await res.json();
    setListResult(data);

    setLoading(false);
  };

  return (
    <div className="vuln-page">
     

      {/* INPUT CARD */}
      <div className="vuln-card">
        <div className="search-row">
          <input
            type="text"
            placeholder="CVE-2007-1508"
            value={cve}
            onChange={(e) => setCve(e.target.value)}
          />
          <button className="search-btn" onClick={fetchCVE}>
            Search
          </button>
        </div>
      </div>

      {/* CVE SEARCH RESULT CARD */}
      <div className="vuln-card">
        <h3 className="card-title">CVE Search Result</h3>
        {searchResult.length === 0 ? (
          <p className="empty">No CVE searched</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>CVE ID</th>
                <th>Description</th>
                <th>Published Date</th>
                <th>Confidence</th>
                <th>Severity</th>
                <th>Recommended Action</th>
                <th>Source</th>
              </tr>
            </thead>
            <tbody>
              {searchResult.map((v, i) => (
                <tr key={i}>
                  <td className="cve-id">{v.cve_id}</td>
                  <td className="desc">{v.description}</td>
                  <td>{v.published_date || "-"}</td>
                  <td>{v.confidence}</td>
                  <td className={`sev ${(v.severity || "LOW").toLowerCase()}`}>
                    {v.severity || "LOW"}
                  </td>
                  <td>{v.recommended_action}</td>
                  <td>{v.source}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* BUTTON CARD */}
      <div className="vuln-card button-card">
        <button
          className={`source-btn ${activeSource === "nvd" ? "active" : ""}`}
          onClick={fetchNVD}
        >
          NVD CVEs
        </button>
        <button
          className={`source-btn ${activeSource === "cisa" ? "active" : ""}`}
          onClick={fetchCISA}
        >
          CISA KEV
        </button>
      </div>

      {/* OUTPUT LIST CARD */}
      <div className="vuln-card">
        <h3 className="card-title">
          {activeSource === "nvd"
            ? "NVD CVE List"
            : activeSource === "cisa"
            ? "CISA KEV List"
            : "CVE Output"}
        </h3>

        {listResult.length === 0 ? (
          <p className="empty">No data loaded</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>CVE ID</th>
                <th>CVSS Score</th>
                <th>Severity</th>
                <th>
                  {activeSource === "nvd"
                    ? "Published Date"
                    : "Exploit Status"}
                </th>
                <th>Source</th>
              </tr>
            </thead>
            <tbody>
              {listResult.map((v, i) => (
                <tr key={i}>
                  <td className="cve-id">{v.cve_id}</td>
                  <td>{v.cvss_score}</td>
                  <td className={`sev ${v.severity?.toLowerCase()}`}>
                    {v.severity}
                  </td>
                  <td>
                    {activeSource === "nvd"
                      ? v.published_date
                      : v.exploit_status}
                  </td>
                  <td>{v.source}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

