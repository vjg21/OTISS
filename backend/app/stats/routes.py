from fastapi import APIRouter
from app.database import get_connection

router = APIRouter()

@router.get("/dashboard")
def dashboard_stats():
    conn = get_connection()
    cur = conn.cursor()

    # ---------- COUNTS ----------
    cur.execute("SELECT COUNT(*) FROM urlhaus_urls;")
    malicious_urls = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM malicious_ips;")
    malicious_ips = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM malware_samples;")
    hashes = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM vulnerabilities;")
    vulnerabilities = cur.fetchone()[0]

    # ---------- TOTAL INDICATORS ----------
    total_indicators = (
        malicious_urls +
        malicious_ips +
        hashes +
        vulnerabilities
    )

    # ---------- HIGH RISK (AUTHENTIC ASSUMPTION) ----------
    # URLHaus + FireHOL IPs + MalwareBazaar hashes
    high_risk = malicious_urls + malicious_ips + hashes

    # ---------- ACTIVE FEEDS ----------
    feeds = []
    if malicious_urls > 0:
        feeds.append("URLHaus")
    if malicious_ips > 0:
        feeds.append("FireHOL")
    if hashes > 0:
        feeds.append("MalwareBazaar")

    # ---------- CLEANUP ----------
    cur.close()
    conn.close()

    return {
        "total_indicators": total_indicators,
        "high_risk": high_risk,
        "malicious_urls": malicious_urls,
        "malicious_ips": malicious_ips,
        "hashes": hashes,
        "vulnerabilities": vulnerabilities,
        "feeds": feeds,
        "status": "OPERATIONAL"
    }
