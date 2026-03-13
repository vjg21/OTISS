import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import get_connection

BASE_DIR = os.path.dirname(__file__)
FIREHOL_FILE = os.path.join(BASE_DIR, "firehol_level1.txt")

def ingest_firehol():
    print("[+] Loading FireHOL Level 1 IP list")

    if not os.path.exists(FIREHOL_FILE):
        print("[!] FireHOL file not found:", FIREHOL_FILE)
        return

    conn = get_connection()
    cur = conn.cursor()
    inserted = 0

    with open(FIREHOL_FILE, "r", encoding="utf-8") as f:
        for line in f:
            ip = line.strip()
            if not ip or ip.startswith("#"):
                continue

            cur.execute(
                """
                INSERT INTO malicious_ips (ip, source)
                VALUES (%s, 'firehol')
                ON CONFLICT DO NOTHING;
                """,
                (ip,)
            )
            inserted += cur.rowcount

    conn.commit()
    cur.close()
    conn.close()

    print(f"[✓] FireHOL ingestion completed. Inserted IPs: {inserted}")
