import sys, os, gzip, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import get_connection

BASE_DIR = os.path.dirname(__file__)
NVD_FILE = os.path.join(BASE_DIR, "..", "temp", "nvdcve-1.1-recent.json.gz")

def ingest_nvd():
    print("[+] Loading NVD CVEs")

    if not os.path.exists(NVD_FILE):
        print("[!] NVD file not found:", NVD_FILE)
        return

    conn = get_connection()
    cur = conn.cursor()
    inserted = 0

    with gzip.open(NVD_FILE, "rt", encoding="utf-8") as f:
        data = json.load(f)

    for item in data.get("vulnerabilities", []):
        cve_id = item.get("cve", {}).get("id")
        if not cve_id:
            continue

        cur.execute(
            """
            INSERT INTO vulnerabilities (cve_id, source)
            VALUES (%s, 'nvd')
            ON CONFLICT DO NOTHING;
            """,
            (cve_id,)
        )
        inserted += cur.rowcount

    conn.commit()
    cur.close()
    conn.close()

    print(f"[✓] NVD ingestion completed. Inserted CVEs: {inserted}")
