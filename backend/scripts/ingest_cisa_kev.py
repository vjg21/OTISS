import sys, os, csv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import get_connection

BASE_DIR = os.path.dirname(__file__)
CISA_FILE = os.path.join(BASE_DIR, "cisa_kev.csv")

def ingest_cisa_kev():
    print("[+] Loading CISA KEV")

    if not os.path.exists(CISA_FILE):
        print("[!] CISA KEV file not found:", CISA_FILE)
        return

    conn = get_connection()
    cur = conn.cursor()
    inserted = 0

    with open(CISA_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cve_id = row.get("cveID")
            due_date = row.get("dueDate")

            if not cve_id:
                continue

            cur.execute(
                """
                INSERT INTO cisa_kev (cve_id, due_date)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
                """,
                (cve_id, due_date)
            )
            inserted += cur.rowcount

    conn.commit()
    cur.close()
    conn.close()

    print(f"[✓] CISA KEV ingestion completed. Inserted rows: {inserted}")
