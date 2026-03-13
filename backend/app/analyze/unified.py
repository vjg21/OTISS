print("🔥 OTISS UNIFIED ANALYZER LOADED 🔥")

from fastapi import APIRouter
from pydantic import BaseModel
from urllib.parse import urlparse
from datetime import datetime
import ipaddress
import re
import dns.resolver

from app.database import get_connection
from app.utils.trusted import is_trusted_indicator

from app.services.otx import query_otx
from app.services.virustotal import query_virustotal
from app.services.urlscan import query_urlscan
from app.services.securitytrails import query_securitytrails

router = APIRouter()

# =========================
# CONFIDENCE WEIGHTS
# =========================
SOURCE_CONFIDENCE = {
    "malwarebazaar": 0.95,
    "firehol": 0.90,
    "urlhaus": 0.85,
    "virustotal": 0.80,
    "urlscan": 0.70,
    "alienvault_otx": 0.60,
    "securitytrails": 0.40,
    "trusted_allowlist": 0.95
}

# =========================
# REQUEST MODEL
# =========================
class UnifiedRequest(BaseModel):
    indicator: str
    use_otx: bool = False
    use_virustotal: bool = False
    use_urlscan: bool = False
    use_securitytrails: bool = False
    use_dns: bool = False

# =========================
# HELPERS
# =========================
def calculate_confidence(sources: list):
    if not sources:
        return 0.65
    scores = [SOURCE_CONFIDENCE.get(s, 0.4) for s in set(sources)]
    return round(min(sum(scores) / len(scores), 0.99), 2)

def determine_verdict(risk_level: str, malicious_hits: int, trusted: bool):
    if malicious_hits >= 2:
        return "MALICIOUS"
    if malicious_hits == 1:
        return "SUSPICIOUS"
    if trusted:
        return "BENIGN"
    return "BENIGN"

def detect_type(value: str):
    value = value.strip().lower()

    try:
        if "/" in value:
            ipaddress.ip_network(value, strict=False)
            return "cidr"
    except:
        pass

    try:
        ipaddress.ip_address(value)
        return "ip"
    except:
        pass

    if re.fullmatch(r"[a-f0-9]{32}|[a-f0-9]{40}|[a-f0-9]{64}", value):
        return "hash"

    if value.startswith("http://") or value.startswith("https://"):
        return "url"

    return "unknown"

def dns_lookup(domain: str):
    data = {"mx": [], "txt": []}
    try:
        for r in dns.resolver.resolve(domain, "MX"):
            data["mx"].append(str(r.exchange).rstrip("."))
    except:
        pass
    try:
        for r in dns.resolver.resolve(domain, "TXT"):
            data["txt"].append("".join(s.decode() for s in r.strings))
    except:
        pass
    return data

# =========================
# CORE ANALYSIS
# =========================
def analyze_indicator(
    indicator: str,
    use_otx=False,
    use_virustotal=False,
    use_urlscan=False,
    use_securitytrails=False,
    use_dns=False
):
    indicator = indicator.strip().lower()
    indicator_type = detect_type(indicator)

    response = {
        "indicator": indicator,
        "type": indicator_type,
        "risk_level": "LOW",
        "confidence": 0.65,
        "verdict": "BENIGN",
        "sources": [],
        "details": {},
        "meta": {
            "analyzed_at": datetime.utcnow().isoformat() + "Z",
            "engine": "OTISS-CTI"
        }
    }

    malicious_hits = 0
    conn = get_connection()
    cur = conn.cursor()

    # =========================
    # HASH → MalwareBazaar
    # =========================
    if indicator_type == "hash":
        cur.execute(
            """
            SELECT malware_family
            FROM malware_samples
            WHERE sha256=%s OR md5=%s OR sha1=%s
            LIMIT 1;
            """,
            (indicator, indicator, indicator)
        )
        row = cur.fetchone()
        if row:
            malicious_hits += 1
            response["sources"].append("malwarebazaar")
            response["details"]["malware_family"] = row[0]

    # =========================
    # IP or CIDR → FireHOL
    # =========================
    elif indicator_type in ("ip", "cidr"):
        cur.execute("SELECT ip, source FROM malicious_ips;")
        rows = cur.fetchall()

        try:
            target = (
                ipaddress.ip_network(indicator, strict=False)
                if indicator_type == "cidr"
                else ipaddress.ip_address(indicator)
            )

            for db_ip, source in rows:
                db_net = ipaddress.ip_network(db_ip, strict=False)

                if (
                    indicator_type == "cidr" and target.subnet_of(db_net)
                ) or (
                    indicator_type == "ip" and target in db_net
                ):
                    malicious_hits += 1
                    response["sources"].append("firehol")
                    response["details"]["blocklist"] = db_ip
                    break
        except:
            pass

    # =========================
    # URL → URLHaus
    # =========================
    elif indicator_type == "url":
        domain = urlparse(indicator).netloc.lower()
        cur.execute(
            """
            SELECT threat, status
            FROM urlhaus_urls
            WHERE host=%s
            LIMIT 1;
            """,
            (domain,)
        )
        row = cur.fetchone()
        if row:
            malicious_hits += 1
            response["sources"].append("urlhaus")
            response["details"]["threat"] = row[0]
            response["details"]["status"] = row[1]

    cur.close()
    conn.close()

    # =========================
    # TRUSTED ALLOWLIST
    # =========================
    trusted, trusted_source = is_trusted_indicator(indicator)
    if trusted:
        response["sources"].append("trusted_allowlist")
        response["details"]["trusted_source"] = trusted_source

    # =========================
    # OPTIONAL ENRICHMENTS
    # =========================
    if use_dns and indicator_type == "url":
        response["details"]["dns"] = dns_lookup(urlparse(indicator).netloc)

    if use_otx:
        otx = query_otx(indicator, indicator_type)
        if otx and otx.get("pulse_info", {}).get("count", 0) > 0:
            malicious_hits += 1
            response["sources"].append("alienvault_otx")

    if use_virustotal:
        vt = query_virustotal(indicator, indicator_type)
        if vt:
            response["sources"].append("virustotal")

    if use_urlscan and indicator_type == "url":
        scan = query_urlscan(indicator)
        if scan and scan.get("verdicts", {}).get("overall", {}).get("malicious"):
            malicious_hits += 1
            response["sources"].append("urlscan")

    if use_securitytrails and indicator_type == "url":
        st = query_securitytrails(urlparse(indicator).netloc)
        if st:
            response["sources"].append("securitytrails")

    # =========================
    # FINAL RISK
    # =========================
    if malicious_hits >= 2:
        response["risk_level"] = "HIGH"
    elif malicious_hits == 1:
        response["risk_level"] = "MEDIUM"

    response["confidence"] = calculate_confidence(response["sources"])
    response["verdict"] = determine_verdict(
        response["risk_level"], malicious_hits, trusted
    )

    return response

# =========================
# ROUTE
# =========================
@router.post("/unified")
def analyze_unified(req: UnifiedRequest):
    return analyze_indicator(
        indicator=req.indicator,
        use_otx=req.use_otx,
        use_virustotal=req.use_virustotal,
        use_urlscan=req.use_urlscan,
        use_securitytrails=req.use_securitytrails,
        use_dns=req.use_dns
    )
