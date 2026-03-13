import "./Help.css";

export default function Help() {
  return (
    <div className="help-page">
     

      <div className="help-card">
        <h3>Dashboard</h3>
        <p>
          The dashboard provides a high-level overview of indicators, threat
          feeds, malicious entities, and system health.
        </p>

        <h3>Analyze</h3>
        <p>
          Use the Analyze page to inspect IPs, URLs, domains, hashes, or CIDR
          ranges. Analysts can enable enrichment sources and review results in
          structured SOC-style tables.
        </p>

        <h3>Vulnerabilities</h3>
        <p>
          Search for individual CVEs or browse NVD and CISA KEV lists. The system
          highlights severity, confidence, and recommended remediation actions.
        </p>

        <h3>Tools</h3>
        <p>
          The Tools section provides categorized access to external threat
          intelligence and security tools. OTISS does not execute tools.
        </p>

        <h3>Risk & Confidence</h3>
        <p>
          Risk levels are calculated based on threat correlations. Confidence
          scores indicate reliability of verdicts and should guide analyst
          decisions.
        </p>

        <h3>Best Practices</h3>
        <ul>
          <li>Always validate indicators using multiple sources</li>
          <li>Prioritize HIGH and CRITICAL risks</li>
          <li>Monitor low-confidence results for false positives</li>
        </ul>
      </div>
    </div>
  );
}
