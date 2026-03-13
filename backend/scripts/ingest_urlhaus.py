import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import get_connection

BASE_DIR = os.path.dirname(__file__)
URLHAUS_FILE = os.path.join(BASE_DIR, "mali_url.txt")

def ingest_urlhaus():
    print("[+] Loading URLHaus feed")

    if not os.path.exists(URLHAUS_FILE):
        print("[!] URLHaus file not found:", URLHAUS_FILE)
        return

    conn = get_connection()
    cur = conn.cursor()
    inserted = 0

    with open(URLHAUS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            url = line.strip()
            if not url:
                continue

            cur.execute(
                """
                INSERT INTO urlhaus_urls (url, threat, status)
                VALUES (%s, 'malware', 'active')
                ON CONFLICT DO NOTHING;
                """,
                (url,)
            )
            inserted += cur.rowcount

    conn.commit()
    cur.close()
    conn.close()

    print(f"[✓] URLHaus ingestion completed. Inserted URLs: {inserted}")
