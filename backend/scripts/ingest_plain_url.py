import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import get_connection

BASE_DIR = os.path.dirname(__file__)
URL_FILE = os.path.join(BASE_DIR, "mali_url.txt")

def ingest_plain_url():
    print("[+] Loading plain malicious URLs")

    if not os.path.exists(URL_FILE):
        print("[!] URL file not found:", URL_FILE)
        return

    conn = get_connection()
    cur = conn.cursor()
    inserted = 0

    with open(URL_FILE, "r", encoding="utf-8") as f:
        for line in f:
            url = line.strip()
            if not url or url.startswith("#"):
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

    print(f"[✓] Plain URL ingestion completed. Inserted URLs: {inserted}")
