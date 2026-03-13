import "./About.css";

export default function About() {
  return (
    <div className="about-page">
      

      <div className="about-card">
        <p>
          <strong>OTISS (Open Threat Intelligence & SOC System)</strong> is a
          SOC-oriented threat intelligence platform built to simulate real-world
          security operations and analyst workflows.
        </p>

        <p>
          The platform aggregates multiple intelligence sources, internal
          databases, and enrichment services to provide actionable insight into
          indicators, vulnerabilities, and infrastructure risks.
        </p>

        <h3>Core Objectives</h3>
        <ul>
          <li>Simulate real Security Operations Center workflows</li>
          <li>Provide accurate IOC & CVE risk assessment</li>
          <li>Use real backend data instead of mock values</li>
          <li>Present results in analyst-friendly formats</li>
        </ul>

        <h3>Key Capabilities</h3>
        <ul>
          <li>Unified & bulk indicator analysis</li>
          <li>Threat feed correlation (URLHaus, FireHOL, MalwareBazaar)</li>
          <li>NVD & CISA KEV vulnerability intelligence</li>
          <li>Confidence-based verdict calculation</li>
        </ul>

        <p>
          <strong>Technology Stack:</strong> React (Vite), FastAPI, PostgreSQL
        </p>

       
      </div>
    </div>
  );
}
