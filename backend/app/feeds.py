import requests
from app.database import get_connection

# =========================
# FIREHOL INGEST
# =========================
def ingest_firehol():
    url = "https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/firehol_level1.netset"
    resp = requests.get(url, timeout=30)

    conn = get_connection()
    cursor = conn.cursor()

    for line in resp.text.splitlines():
        if not line or line.startswith("#"):
            continue

        cursor.execute(
            """
            INSERT INTO malicious_ips (ip, source)
            VALUES (%s, 'FireHOL')
            ON CONFLICT DO NOTHING;
            """,
            (line.strip(),)
        )

    conn.commit()
    cursor.close()
    conn.close()

# =========================
# URLHAUS INGEST
# =========================
def ingest_urlhaus():
    url = "https://urlhaus.abuse.ch/downloads/text_online/"
    resp = requests.get(url, timeout=30)

    conn = get_connection()
    cursor = conn.cursor()

    for line in resp.text.splitlines():
        if not line or line.startswith("#"):
            continue

        cursor.execute(
            """
            INSERT INTO urlhaus_urls (url, threat, status)
            VALUES (%s, 'malware', 'online')
            ON CONFLICT DO NOTHING;
            """,
            (line.strip(),)
        )

    conn.commit()
    cursor.close()
    conn.close()
